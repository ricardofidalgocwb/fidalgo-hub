"""Máquina de status da Fila Editorial (schema Notion ao vivo).

Aprovar: Rascunho|Aguardando OK → Aprovado.
Aprovar NUNCA publica (IG / site / n8n / webhook).
Publicado só o Founder marca — este runner não tem ação publicar.
Adiar não inventa status Adiado (não existe no schema): volta a Rascunho.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

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

ACTION_APROVAR = "aprovar"
ACTION_RECUSAR = "recusar"
ACTION_ADIAR = "adiar"
ACTION_PUBLICAR = "publicar"
ACTION_NOVO = "novo"

ACTIONS = (ACTION_APROVAR, ACTION_RECUSAR, ACTION_ADIAR, ACTION_NOVO)

BRACO_EDITORA = "Editora"
BRACO_PRODUTORA = "Produtora"
BRACO_OPTIONS = (BRACO_EDITORA, BRACO_PRODUTORA)

PORTA_VENDA = "Venda"
PORTA_CLUBE = "Clube"
PORTA_INTERNO = "Interno"
PORTA_OPTIONS = (PORTA_VENDA, PORTA_CLUBE, PORTA_INTERNO)

FORMATO_OPTIONS = (
    "Almanaque",
    "Módulo",
    "Ficha",
    "Reel",
    "Carrossel",
    "Post",
)

CANAL_NAO_PUBLICAR = "Não publicar"
CANAL_OPTIONS = (CANAL_NAO_PUBLICAR, "IG", "Clube", "PDF", "Site")

PROP_STATUS = "Status"
PROP_OBSERVACOES = "Observações"
PROP_PROXIMA = "Próxima ação"
PROP_CANAL = "Canal"
PROP_BRACO = "Braço"
PROP_PORTA = "Porta"
PROP_FORMATO = "Formato"
PROP_PECA = "Peça"
PROP_AUTOMACAO = "Automação executada"

MIN_RECUSA_REASON = 8

ALLOWED_WRITE_PROPERTIES = frozenset(
    {PROP_STATUS, PROP_OBSERVACOES, PROP_PROXIMA}
)
ALLOWED_CREATE_PROPERTIES = frozenset(
    {
        PROP_PECA,
        PROP_BRACO,
        PROP_PORTA,
        PROP_STATUS,
        PROP_FORMATO,
        PROP_CANAL,
        PROP_AUTOMACAO,
        PROP_OBSERVACOES,
        PROP_PROXIMA,
    }
)

FORBIDDEN_AGENTS = ("AGT-09", "7º bot Grok", "7th Grok")
AGENTS = {
    BRACO_EDITORA: "Acervo",
    BRACO_PRODUTORA: "Comunicação",
}


class TransitionError(ValueError):
    """Transição inválida, canon recusado ou payload fora do contrato."""


def assert_not_forbidden_agent(name: str | None) -> None:
    if not name:
        return
    blob = name.lower()
    for banned in FORBIDDEN_AGENTS:
        if banned.lower() in blob:
            raise TransitionError(
                f"{banned} não faz parte desta mesa. Staff cheio (6)."
            )


@dataclass(frozen=True)
class Transition:
    action: str
    from_status: str | None
    to_status: str
    properties: dict[str, Any]
    fire_n8n: bool
    fire_instagram: bool
    fire_site: bool
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
            "fire_instagram": self.fire_instagram,
            "fire_site": self.fire_site,
            "log_only": self.log_only,
        }
        if page_id:
            payload["page_id"] = page_id
        if self.reason:
            payload["reason"] = self.reason
        if self.notes:
            payload["notes"] = list(self.notes)
        return payload


def _rich_text(content: str) -> dict[str, Any]:
    return {"rich_text": [{"type": "text", "text": {"content": content[:1900]}}]}


def _select(name: str) -> dict[str, Any]:
    return {"select": {"name": name}}


def _assert_known_status(status: str) -> None:
    if status not in PIPELINE_STATUSES:
        raise TransitionError(f"Status desconhecido: {status!r}")


def _side_channels_off() -> dict[str, bool]:
    return {
        "fire_n8n": False,
        "fire_instagram": False,
        "fire_site": False,
    }


def build_transition(
    action: str,
    current_status: str | None,
    *,
    reason: str | None = None,
    peca: str | None = None,
    metrica: str | None = None,
    observacoes: str | None = None,
    proxima_acao: str | None = None,
    braco: str | None = None,
    porta: str | None = None,
    formato: str | None = None,
) -> Transition:
    """Monta o PATCH/create da Fila Editorial. Sem efeito colateral."""
    action = (action or "").strip().lower()
    if action == ACTION_PUBLICAR:
        raise TransitionError(
            "Publicado só o Founder marca. O runner editorial não publica."
        )
    if action not in ACTIONS:
        raise TransitionError(f"Ação desconhecida: {action!r}")

    if action == ACTION_NOVO:
        return _build_create(
            peca=peca,
            braco=braco,
            porta=porta,
            formato=formato,
            observacoes=observacoes,
            proxima_acao=proxima_acao,
            metrica=metrica,
        )

    if not current_status:
        raise TransitionError("Status atual é obrigatório.")
    _assert_known_status(current_status)
    if current_status == STATUS_PUBLICADO:
        raise TransitionError(
            "Card já Publicado — o runner não mexe. Founder é o dono desse status."
        )

    from editorial.canon import assert_card_canon

    if action == ACTION_APROVAR:
        if current_status not in {STATUS_RASCUNHO, STATUS_AGUARDANDO}:
            raise TransitionError(
                f"Aprovar só vale de {STATUS_RASCUNHO!r} ou "
                f"{STATUS_AGUARDANDO!r} (atual: {current_status!r})"
            )
        assert_card_canon(
            peca=peca,
            metrica=metrica,
            observacoes=observacoes,
            proxima_acao=proxima_acao,
        )
        return Transition(
            action=action,
            from_status=current_status,
            to_status=STATUS_APROVADO,
            properties={PROP_STATUS: _select(STATUS_APROVADO)},
            log_only=True,
            notes=(
                "Aprovar não publica. Sem IG, sem site, sem n8n, sem webhook.",
                "Publicado continua sendo status do Founder.",
                "Automação executada não é marcada.",
            ),
            **_side_channels_off(),
        )

    if action == ACTION_RECUSAR:
        if current_status not in {
            STATUS_RASCUNHO,
            STATUS_AGUARDANDO,
            STATUS_APROVADO,
        }:
            raise TransitionError(
                f"Recusar só vale a partir de {STATUS_RASCUNHO!r}, "
                f"{STATUS_AGUARDANDO!r} ou {STATUS_APROVADO!r}"
            )
        cleaned = (reason or "").strip()
        if len(cleaned) < MIN_RECUSA_REASON:
            raise TransitionError(
                f"Recusar exige motivo curto (mínimo {MIN_RECUSA_REASON} caracteres)"
            )
        obs = f"[Recusa Mesa] {cleaned}"
        return Transition(
            action=action,
            from_status=current_status,
            to_status=STATUS_RECUSADO,
            properties={
                PROP_STATUS: _select(STATUS_RECUSADO),
                PROP_OBSERVACOES: _rich_text(obs),
            },
            log_only=True,
            reason=cleaned,
            notes=("Recusar não publica e não dispara n8n/IG.",),
            **_side_channels_off(),
        )

    # Adiar: schema vivo não tem Adiado. Volta a Rascunho + nota.
    if current_status not in {STATUS_RASCUNHO, STATUS_AGUARDANDO, STATUS_APROVADO}:
        raise TransitionError(
            f"Adiar só vale a partir de {STATUS_RASCUNHO!r}, "
            f"{STATUS_AGUARDANDO!r} ou {STATUS_APROVADO!r}"
        )
    cleaned = (reason or "").strip()
    props: dict[str, Any] = {PROP_STATUS: _select(STATUS_RASCUNHO)}
    note = f"[Adiado Mesa] {cleaned}" if cleaned else "[Adiado Mesa]"
    props[PROP_OBSERVACOES] = _rich_text(note)
    props[PROP_PROXIMA] = _rich_text("Adiado — reabrir quando a mesa pedir.")
    return Transition(
        action=ACTION_ADIAR,
        from_status=current_status,
        to_status=STATUS_RASCUNHO,
        properties=props,
        log_only=True,
        reason=cleaned or None,
        notes=(
            "Adiar não inventa status Adiado (não existe na Fila Editorial).",
            "Volta a Rascunho. Não publica.",
        ),
        **_side_channels_off(),
    )


def _build_create(
    *,
    peca: str | None,
    braco: str | None,
    porta: str | None,
    formato: str | None,
    observacoes: str | None,
    proxima_acao: str | None,
    metrica: str | None,
) -> Transition:
    title = (peca or "").strip()
    if not title:
        raise TransitionError("Card novo exige Peça (título).")
    if braco not in BRACO_OPTIONS:
        raise TransitionError(f"Braço deve ser Editora ou Produtora (recebido: {braco!r})")
    if formato not in FORMATO_OPTIONS:
        raise TransitionError(f"Formato desconhecido: {formato!r}")
    porta_name = porta or PORTA_INTERNO
    if porta_name not in PORTA_OPTIONS:
        raise TransitionError(f"Porta desconhecida: {porta_name!r}")

    from editorial.canon import assert_card_canon

    assert_card_canon(
        peca=title,
        metrica=metrica,
        observacoes=observacoes,
        proxima_acao=proxima_acao,
    )

    props: dict[str, Any] = {
        PROP_PECA: {"title": [{"type": "text", "text": {"content": title[:200]}}]},
        PROP_BRACO: _select(braco),
        PROP_PORTA: _select(porta_name),
        PROP_STATUS: _select(STATUS_RASCUNHO),
        PROP_FORMATO: _select(formato),
        PROP_CANAL: _select(CANAL_NAO_PUBLICAR),
        PROP_AUTOMACAO: {"checkbox": False},
    }
    if observacoes and observacoes.strip():
        props[PROP_OBSERVACOES] = _rich_text(observacoes.strip())
    if proxima_acao and proxima_acao.strip():
        props[PROP_PROXIMA] = _rich_text(proxima_acao.strip())

    return Transition(
        action=ACTION_NOVO,
        from_status=None,
        to_status=STATUS_RASCUNHO,
        properties=props,
        log_only=True,
        notes=(
            "Card novo: Canal = Não publicar. Status = Rascunho.",
            "Automação executada = false. Nada no ar.",
        ),
        **_side_channels_off(),
    )


def assert_editorial_only_payload(
    properties: Mapping[str, Any], *, creating: bool = False
) -> None:
    allowed = ALLOWED_CREATE_PROPERTIES if creating else ALLOWED_WRITE_PROPERTIES
    extra = set(properties) - allowed
    if extra:
        raise TransitionError(
            f"Escrita fora das propriedades da Fila Editorial: {sorted(extra)}"
        )


def assert_never_publicado(properties: Mapping[str, Any]) -> None:
    status = (properties.get(PROP_STATUS) or {}).get("select", {}).get("name")
    if status == STATUS_PUBLICADO:
        raise TransitionError(
            "Proibido gravar Status Publicado neste runner. Só o Founder marca."
        )


def assert_never_automacao_true(properties: Mapping[str, Any]) -> None:
    auto = properties.get(PROP_AUTOMACAO)
    if isinstance(auto, dict) and auto.get("checkbox") is True:
        raise TransitionError(
            "Aprovar/ações da mesa não marcam Automação executada."
        )


def assert_canal_nao_publicar_on_create(properties: Mapping[str, Any]) -> None:
    canal = (properties.get(PROP_CANAL) or {}).get("select", {}).get("name")
    if canal and canal != CANAL_NAO_PUBLICAR:
        raise TransitionError(
            f"Card novo exige Canal = {CANAL_NAO_PUBLICAR!r} (recebido: {canal!r})"
        )


def publish_allowed_for_action(action: str) -> bool:
    """Sempre False. Aprovar nunca publica; não existe ação publicar."""
    del action
    return False
