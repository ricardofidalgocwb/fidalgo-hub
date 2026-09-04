"""Máquina de status da Fila Editorial (Editora × Produtora · Heros).

Aprovar ≠ publicar. O runner nunca define Status=Publicado, nunca muda Canal,
nunca dispara n8n, nunca escreve Fila Founder / OS / CRM / Clientes / Financeiro.
Publicado é estado humano/Ricardo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from dashboard.ids import (
    CLIENTES_ID,
    CRM_OPORTUNIDADES_ID,
    FILA_EDITORIAL_ID,
    FILA_FOUNDER_ID,
    FINANCEIRO_ID,
    FORBIDDEN_EDITORIAL_WRITE_IDS,
    OS_DATABASE_ID,
)

STATUS_RASCUNHO = "Rascunho"
STATUS_AGUARDANDO = "Aguardando OK"
STATUS_APROVADO = "Aprovado"
STATUS_PUBLICADO = "Publicado"
STATUS_RECUSADO = "Recusado"

PIPELINE_STATUSES = (
    STATUS_RASCUNHO,
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
    STATUS_PUBLICADO,
    STATUS_RECUSADO,
)

APPROVABLE_STATUSES = frozenset({STATUS_RASCUNHO, STATUS_AGUARDANDO})
REFUSABLE_STATUSES = frozenset({STATUS_RASCUNHO, STATUS_AGUARDANDO, STATUS_APROVADO})

ACTION_APROVAR = "aprovar"
ACTION_RECUSAR = "recusar"
ACTIONS = (ACTION_APROVAR, ACTION_RECUSAR)

PROP_STATUS = "Status"
PROP_OBSERVACOES = "Observações"
PROP_CANAL = "Canal"
PROP_AUTOMACAO = "Automação executada"

CANAL_NAO_PUBLICAR = "Não publicar"

ALLOWED_WRITE_PROPERTIES = frozenset({PROP_STATUS, PROP_OBSERVACOES})

FORBIDDEN_WRITE_PROPERTIES = frozenset(
    {
        "Peça",
        "Nº",
        "Braço",
        PROP_CANAL,
        "Formato",
        "Porta",
        "Métrica",
        "Próxima ação",
        "Data",
        PROP_AUTOMACAO,
    }
)

MIN_RECUSA_REASON = 8

RULE_APROVAR_NAO_PUBLICA = (
    "Aprovar ≠ publicar. Canal Não publicar permanece. "
    "Publicado só o Ricardo. Sem n8n, IG, PDF ou site."
)


class EditorialError(ValueError):
    """Transição inválida, payload proibido ou database errada."""


@dataclass(frozen=True)
class EditorialTransition:
    action: str
    from_status: str
    to_status: str
    properties: dict[str, Any]
    fire_n8n: bool = False
    publish: bool = False
    canal_unchanged: str | None = None
    reason: str | None = None
    notes: tuple[str, ...] = field(default_factory=tuple)

    def as_log_dict(self, page_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "action": self.action,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "properties": self.properties,
            "fire_n8n": self.fire_n8n,
            "publish": self.publish,
        }
        if page_id:
            payload["page_id"] = page_id
        if self.canal_unchanged is not None:
            payload["canal_unchanged"] = self.canal_unchanged
        if self.reason:
            payload["reason"] = self.reason
        if self.notes:
            payload["notes"] = list(self.notes)
        return payload


def _rich_text(content: str) -> dict[str, Any]:
    return {"rich_text": [{"type": "text", "text": {"content": content[:1900]}}]}


def _normalize_id(value: str) -> str:
    return (value or "").strip().lower()


def _compact(value: str) -> str:
    return _normalize_id(value).replace("-", "")


def build_transition(
    action: str,
    current_status: str,
    *,
    reason: str | None = None,
    canal: str | None = None,
    peca: str | None = None,
    metrica: str | None = None,
    observacoes: str | None = None,
    proxima_acao: str | None = None,
) -> EditorialTransition:
    """Monta o PATCH da Fila Editorial. Sem efeito colateral. Nunca Publicado."""
    action = (action or "").strip().lower()
    if action in {"publicar", "publish"}:
        raise EditorialError(
            "O runner recusa publicar. Publicado é estado humano/Ricardo."
        )
    if action not in ACTIONS:
        raise EditorialError(f"Ação desconhecida: {action!r}")
    if current_status == STATUS_PUBLICADO:
        raise EditorialError(
            "Publicado é estado humano/Ricardo. O runner não altera peças publicadas."
        )
    if current_status not in PIPELINE_STATUSES:
        raise EditorialError(f"Status desconhecido: {current_status!r}")

    if action == ACTION_APROVAR:
        if current_status not in APPROVABLE_STATUSES:
            raise EditorialError(
                f"Aprovar só vale de {STATUS_RASCUNHO!r} ou {STATUS_AGUARDANDO!r} "
                f"(atual: {current_status!r})"
            )
        from dashboard.editorial_canon import assert_card_canon

        assert_card_canon(
            peca=peca,
            metrica=metrica,
            observacoes=observacoes,
            proxima_acao=proxima_acao,
        )
        props: dict[str, Any] = {
            PROP_STATUS: {"select": {"name": STATUS_APROVADO}},
        }
        cleaned = (reason or "").strip()
        if cleaned:
            props[PROP_OBSERVACOES] = _rich_text(f"[Aprovado editorial] {cleaned}")
        transition = EditorialTransition(
            action=action,
            from_status=current_status,
            to_status=STATUS_APROVADO,
            properties=props,
            fire_n8n=False,
            publish=False,
            canal_unchanged=canal or CANAL_NAO_PUBLICAR,
            reason=cleaned or None,
            notes=(RULE_APROVAR_NAO_PUBLICA,),
        )
        assert_editorial_only_payload(transition.properties)
        assert_never_publicado(transition.properties)
        assert_n8n_never(transition)
        return transition

    cleaned = (reason or "").strip()
    if len(cleaned) < MIN_RECUSA_REASON:
        raise EditorialError(
            f"Recusar exige motivo curto (mínimo {MIN_RECUSA_REASON} caracteres)"
        )
    if current_status not in REFUSABLE_STATUSES:
        raise EditorialError(
            f"Recusar só vale a partir de {STATUS_RASCUNHO!r}, "
            f"{STATUS_AGUARDANDO!r} ou {STATUS_APROVADO!r}"
        )
    transition = EditorialTransition(
        action=ACTION_RECUSAR,
        from_status=current_status,
        to_status=STATUS_RECUSADO,
        properties={
            PROP_STATUS: {"select": {"name": STATUS_RECUSADO}},
            PROP_OBSERVACOES: _rich_text(f"[Recusa editorial] {cleaned}"),
        },
        fire_n8n=False,
        publish=False,
        canal_unchanged=canal or CANAL_NAO_PUBLICAR,
        reason=cleaned,
        notes=("Recusar não publica e não dispara n8n.",),
    )
    assert_editorial_only_payload(transition.properties)
    assert_never_publicado(transition.properties)
    assert_n8n_never(transition)
    return transition


def assert_editorial_only_payload(properties: Mapping[str, Any]) -> None:
    extra = set(properties) - ALLOWED_WRITE_PROPERTIES
    if extra:
        raise EditorialError(
            f"Escrita fora das propriedades permitidas da Fila Editorial: {sorted(extra)}"
        )
    forbidden = set(properties) & FORBIDDEN_WRITE_PROPERTIES
    if forbidden:
        raise EditorialError(
            f"Proibido alterar {sorted(forbidden)} neste runner "
            f"(Canal Não publicar permanece; sem automação de publicação)."
        )


def assert_never_publicado(properties: Mapping[str, Any]) -> None:
    status = (properties.get(PROP_STATUS) or {}).get("select") or {}
    name = status.get("name")
    if name == STATUS_PUBLICADO:
        raise EditorialError(
            "Publicado é estado humano/Ricardo. O runner recusa definir Publicado."
        )
    canal = (properties.get(PROP_CANAL) or {}).get("select") or {}
    if PROP_CANAL in properties or canal.get("name"):
        raise EditorialError(
            "Runner não altera Canal. Canal 'Não publicar' permanece."
        )
    if PROP_AUTOMACAO in properties:
        raise EditorialError("Runner não marca Automação executada.")


def assert_n8n_never(transition: EditorialTransition) -> None:
    if transition.fire_n8n or transition.publish:
        raise EditorialError("Runner editorial nunca dispara n8n nem publica.")


def assert_editorial_database_only(database_id: str) -> None:
    target = _compact(database_id)
    if target != _compact(FILA_EDITORIAL_ID):
        raise EditorialError(
            "Runner editorial só escreve na Fila Editorial "
            "(8af724e1…). Não toca Fila Founder, OS, CRM, Clientes ou Financeiro."
        )
    forbidden = {_compact(db_id) for db_id in FORBIDDEN_EDITORIAL_WRITE_IDS}
    if target in forbidden:
        raise EditorialError(
            "Proibido escrever em Fila Founder, OS, CRM, Clientes ou Financeiro."
        )


def n8n_allowed_for_editorial_action(_action: str) -> bool:
    """Contrato: editorial nunca dispara n8n, em nenhuma ação."""
    return False


def empty_counts() -> dict[str, int]:
    return {status: 0 for status in PIPELINE_STATUSES}


def planned_approve_actions(cards: list[Mapping[str, Any]]) -> list[EditorialTransition]:
    planned: list[EditorialTransition] = []
    for card in cards:
        status = (card.get("status") or "").strip()
        if status not in APPROVABLE_STATUSES:
            continue
        planned.append(
            build_transition(
                ACTION_APROVAR,
                status,
                canal=card.get("canal") or CANAL_NAO_PUBLICAR,
                peca=card.get("peca"),
                metrica=card.get("metrica"),
                observacoes=card.get("observacoes"),
                proxima_acao=card.get("proxima_acao"),
            )
        )
    return planned


# Reexporta IDs usados nos testes de guarda (não misturar com Founder).
FORBIDDEN_DB_LABELS = {
    FILA_FOUNDER_ID: "Fila Founder",
    OS_DATABASE_ID: "OS",
    CRM_OPORTUNIDADES_ID: "CRM",
    CLIENTES_ID: "Clientes",
    FINANCEIRO_ID: "Financeiro",
}
