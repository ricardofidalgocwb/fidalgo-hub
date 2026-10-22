"""Entidades do grupo e a máquina de status da OS industrial."""

from __future__ import annotations

from config.entidades import AI, CENTRO_EF, EF, ENTIDADES, FSE, HC, PF
from core.errors import EntityIsolationError, TransitionError, ValidationError

STATUS_EXIGE_EVIDENCIA = frozenset({"Teste de Carga", "Faturado"})

CENTROS_POR_ENTIDADE: dict[str, tuple[str, ...]] = {
    AI: (f"{AI}-OPEX",),
    HC: (f"{HC}-OPEX",),
    FSE: (f"{FSE}-OPEX", f"{FSE}-CAPEX"),
    EF: (CENTRO_EF,),
    PF: (f"{PF}-OPEX",),
}

TIPOS_EQUIPAMENTO: tuple[str, ...] = (
    "Transformador",
    "Motor Elétrico",
    "Gerador",
    "Disjuntor",
)

STATUS_OS: tuple[str, ...] = (
    "Orçamento",
    "Aprovado",
    "Em Manutenção",
    "Teste de Carga",
    "Faturado",
)

STATUS_INICIAL_OS = "Orçamento"
STATUS_INICIAL_EQUIPAMENTO = "Diagnóstico"

TRANSICOES: dict[str, frozenset[str]] = {
    "Orçamento": frozenset({"Aprovado"}),
    "Aprovado": frozenset({"Em Manutenção"}),
    "Em Manutenção": frozenset({"Teste de Carga"}),
    "Teste de Carga": frozenset({"Faturado"}),
    "Faturado": frozenset(),
}


def validar_entidade(entidade: str) -> str:
    if entidade not in ENTIDADES:
        raise ValidationError("entidade desconhecida")
    return entidade


def validar_tipo_equipamento(tipo: str) -> str:
    if tipo not in TIPOS_EQUIPAMENTO:
        raise ValidationError("tipo de equipamento nao permitido")
    return tipo


def centro_padrao(entidade: str) -> str:
    """Centro inicial da entidade. EF nasce em EF-OPEX; as outras não herdam esse código."""
    validar_entidade(entidade)
    return CENTROS_POR_ENTIDADE[entidade][0]


def resolver_centro(entidade: str, centro: str | None) -> str:
    validar_entidade(entidade)
    permitidos = CENTROS_POR_ENTIDADE[entidade]
    if entidade == EF:
        if centro not in (None, "", CENTRO_EF):
            raise EntityIsolationError(f"{EF} exige centro_custo {CENTRO_EF}")
        return CENTRO_EF
    if centro in (None, ""):
        return permitidos[0]
    if centro == CENTRO_EF or centro not in permitidos:
        raise EntityIsolationError("centro_custo incompativel com a entidade")
    return centro


def proximos_status(status_atual: str) -> list[str]:
    if status_atual not in TRANSICOES:
        raise TransitionError("status de OS desconhecido")
    return [status for status in STATUS_OS if status in TRANSICOES[status_atual]]


def assert_transicao(origem: str, destino: str) -> None:
    if origem not in TRANSICOES or destino not in TRANSICOES:
        raise TransitionError("status de OS desconhecido")
    if destino not in TRANSICOES[origem]:
        raise TransitionError(f"transicao invalida: {origem} -> {destino}")
