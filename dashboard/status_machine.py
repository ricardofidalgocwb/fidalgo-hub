"""Máquina de status da Fila Founder (schema Notion ao vivo).

Aprovar nunca dispara n8n. n8n só pode ser considerado em Avançar,
e mesmo assim fica desligado por padrão (env).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping

STATUS_AGUARDANDO = "Aguardando OK"
STATUS_APROVADO = "Aprovado"
STATUS_EM_EXECUCAO = "Em Execução"
STATUS_CONCLUIDO = "Concluído"
STATUS_REJEITADO = "Rejeitado"
STATUS_ADIADO = "Adiado"

PIPELINE_STATUSES = (
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
    STATUS_EM_EXECUCAO,
    STATUS_CONCLUIDO,
    STATUS_REJEITADO,
    STATUS_ADIADO,
)

ACTION_APROVAR = "aprovar"
ACTION_AVANCAR = "avancar"
ACTION_RECUSAR = "recusar"
ACTION_ADIAR = "adiar"

ACTIONS = (ACTION_APROVAR, ACTION_AVANCAR, ACTION_RECUSAR, ACTION_ADIAR)

FILA_L0 = "1 · L0"
FILA_P0 = "2 · P0/Crítica"
FILA_CAIXA = "3 · Caixa"
FILA_DEMAIS = "4 · Demais"

FILA_ORDER = (FILA_L0, FILA_P0, FILA_CAIXA, FILA_DEMAIS)

PRIORIDADE_ORDER = ("Crítica", "Alta", "Média", "Baixa")

PROP_STATUS = "Status"
PROP_DATA_OK = "Data do OK"
PROP_OBSERVACOES = "Observações"

MIN_RECUSA_REASON = 8

ALLOWED_WRITE_PROPERTIES = frozenset({PROP_STATUS, PROP_DATA_OK, PROP_OBSERVACOES})

OS_STATUS_ENTREGUE = "Entregue"
ARCHIVED_LEADS_PREFIX = "43b3f514"


class TransitionError(ValueError):
    """Transição inválida ou payload incompleto."""


@dataclass(frozen=True)
class Transition:
    action: str
    from_status: str
    to_status: str
    properties: dict[str, Any]
    fire_n8n: bool
    log_only: bool
    reason: str | None = None
    notes: tuple[str, ...] = field(default_factory=tuple)

    def as_log_dict(self, page_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "action": self.action,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "properties": self.properties,
            "fire_n8n": self.fire_n8n,
            "log_only": self.log_only,
        }
        if page_id:
            payload["page_id"] = page_id
        if self.reason:
            payload["reason"] = self.reason
        if self.notes:
            payload["notes"] = list(self.notes)
        return payload


def _today(today: date | None = None) -> str:
    return (today or date.today()).isoformat()


def _rich_text(content: str) -> dict[str, Any]:
    return {"rich_text": [{"type": "text", "text": {"content": content[:1900]}}]}


def _assert_known_status(status: str) -> None:
    if status not in PIPELINE_STATUSES:
        raise TransitionError(f"Status desconhecido: {status!r}")


def build_transition(
    action: str,
    current_status: str,
    *,
    reason: str | None = None,
    today: date | None = None,
    n8n_avancar_enabled: bool = False,
) -> Transition:
    """Monta o PATCH de propriedades da Fila Founder. Sem efeito colateral."""
    action = (action or "").strip().lower()
    if action not in ACTIONS:
        raise TransitionError(f"Ação desconhecida: {action!r}")
    _assert_known_status(current_status)

    if action == ACTION_APROVAR:
        if current_status != STATUS_AGUARDANDO:
            raise TransitionError(
                f"Aprovar só vale de {STATUS_AGUARDANDO!r} (atual: {current_status!r})"
            )
        props = {
            PROP_STATUS: {"select": {"name": STATUS_APROVADO}},
            PROP_DATA_OK: {"date": {"start": _today(today)}},
        }
        return Transition(
            action=action,
            from_status=current_status,
            to_status=STATUS_APROVADO,
            properties=props,
            fire_n8n=False,
            log_only=True,
            notes=(
                "Aprovar não dispara n8n. Execução só depois de Avançar.",
            ),
        )

    if action == ACTION_AVANCAR:
        if current_status != STATUS_APROVADO:
            raise TransitionError(
                f"Avançar só vale de {STATUS_APROVADO!r} (atual: {current_status!r})"
            )
        fire = bool(n8n_avancar_enabled)
        notes = ["Avançar registra Em Execução no Notion."]
        if fire:
            notes.append("Webhook n8n opcional habilitado via env (N8N_AVANCAR_ENABLED=1).")
        else:
            notes.append("n8n desligado (padrão). Apenas log.")
        return Transition(
            action=action,
            from_status=current_status,
            to_status=STATUS_EM_EXECUCAO,
            properties={PROP_STATUS: {"select": {"name": STATUS_EM_EXECUCAO}}},
            fire_n8n=fire,
            log_only=not fire,
            notes=tuple(notes),
        )

    if action == ACTION_RECUSAR:
        if current_status not in {STATUS_AGUARDANDO, STATUS_APROVADO}:
            raise TransitionError(
                f"Recusar só vale a partir de {STATUS_AGUARDANDO!r} ou {STATUS_APROVADO!r}"
            )
        cleaned = (reason or "").strip()
        if len(cleaned) < MIN_RECUSA_REASON:
            raise TransitionError(
                f"Recusar exige motivo curto (mínimo {MIN_RECUSA_REASON} caracteres)"
            )
        obs = f"[Recusa Founder] {cleaned}"
        return Transition(
            action=action,
            from_status=current_status,
            to_status=STATUS_REJEITADO,
            properties={
                PROP_STATUS: {"select": {"name": STATUS_REJEITADO}},
                PROP_DATA_OK: {"date": {"start": _today(today)}},
                PROP_OBSERVACOES: _rich_text(obs),
            },
            fire_n8n=False,
            log_only=True,
            reason=cleaned,
            notes=("Aprovar/Recusar não disparam n8n.",),
        )

    if current_status not in {STATUS_AGUARDANDO, STATUS_APROVADO}:
        raise TransitionError(
            f"Adiar só vale a partir de {STATUS_AGUARDANDO!r} ou {STATUS_APROVADO!r}"
        )
    props: dict[str, Any] = {
        PROP_STATUS: {"select": {"name": STATUS_ADIADO}},
        PROP_DATA_OK: {"date": {"start": _today(today)}},
    }
    cleaned = (reason or "").strip()
    if cleaned:
        props[PROP_OBSERVACOES] = _rich_text(f"[Adiado Founder] {cleaned}")
    return Transition(
        action=ACTION_ADIAR,
        from_status=current_status,
        to_status=STATUS_ADIADO,
        properties=props,
        fire_n8n=False,
        log_only=True,
        reason=cleaned or None,
        notes=("Adiar não dispara n8n.",),
    )


def assert_fila_founder_only_payload(properties: Mapping[str, Any]) -> None:
    extra = set(properties) - ALLOWED_WRITE_PROPERTIES
    if extra:
        raise TransitionError(
            f"Escrita fora das propriedades da Fila Founder: {sorted(extra)}"
        )


def assert_not_os_entregue_writer(database_id: str, properties: Mapping[str, Any]) -> None:
    """Guarda: este painel nunca escreve Status Entregue em OS."""
    from dashboard.ids import OS_DATABASE_ID

    if _normalize_id(database_id) == _normalize_id(OS_DATABASE_ID):
        raise TransitionError("Painel Founder não escreve na database de OS.")
    status = (
        properties.get(PROP_STATUS, {})
        .get("select", {})
        .get("name")
    )
    if status == OS_STATUS_ENTREGUE:
        raise TransitionError("Proibido escrever OS Status Entregue neste painel.")


def assert_not_archived_leads(database_id: str) -> None:
    compact = _normalize_id(database_id).replace("-", "")
    if compact.startswith(ARCHIVED_LEADS_PREFIX):
        raise TransitionError(
            "Leads arquivado 43b3f514 é proibido. CRM SSOT = 6157d36b…"
        )


def n8n_allowed_for_action(action: str, n8n_avancar_enabled: bool) -> bool:
    """Aprovar nunca retorna True, mesmo com webhook configurado."""
    if action != ACTION_AVANCAR:
        return False
    return bool(n8n_avancar_enabled)


def fila_sort_key(fila: str | None, nivel_l: str | None, prioridade: str | None) -> tuple:
    fila_idx = FILA_ORDER.index(fila) if fila in FILA_ORDER else len(FILA_ORDER)
    nivel_idx = _nivel_index(nivel_l)
    prio_idx = PRIORIDADE_ORDER.index(prioridade) if prioridade in PRIORIDADE_ORDER else len(PRIORIDADE_ORDER)
    return (fila_idx, nivel_idx, prio_idx)


def _nivel_index(nivel_l: str | None) -> int:
    if not nivel_l:
        return 99
    order = (
        "L0 Segurança",
        "L1 Compliance",
        "L2 Dado",
        "L3 Promessa",
        "L4 Caixa/Margem",
        "L5 Comercial",
        "L6 Interno",
    )
    return order.index(nivel_l) if nivel_l in order else 99


def _normalize_id(value: str) -> str:
    return (value or "").strip().lower()


def flags_heros_vs_fse(title: str, recomendacao: str = "", fila: str | None = None) -> str | None:
    blob = f"{title} {recomendacao}".upper()
    mentions_fse = "FSE" in blob
    mentions_heros = "HEROS" in blob
    if fila == FILA_CAIXA and mentions_fse and mentions_heros:
        return "Não misturar CNPJ/caixa Heros vs FSE neste card."
    if fila == FILA_CAIXA and mentions_fse:
        return "Card de Caixa cita FSE — conferir CNPJ/caixa separado da Heros Custom."
    return None
