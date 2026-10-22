"""Única lista de tags de caixa e o centro padrão da EF.

O schema, o RNA Atlas e o CSV importam daqui. Não copie a tupla.
"""

from __future__ import annotations

EF = "EF"
FSE = "FSE"
HC = "HC"
AI = "AI"
PF = "PF"

ENTIDADES: tuple[str, ...] = (EF, FSE, HC, AI, PF)
CENTRO_EF = "EF-OPEX"

_MARCA_CHECK = "{{CHECK_ENTIDADE}}"
_MARCA_CENTRO = "{{CENTRO_EF}}"


def check_entidade_sql() -> str:
    lista = ", ".join(f"'{tag}'" for tag in ENTIDADES)
    return f"CHECK (entidade IN ({lista}))"


def render_schema(sql: str) -> str:
    """Aplica a lista de tags e o centro EF no texto do schema."""
    if sql.count(_MARCA_CHECK) != 5:
        raise RuntimeError("schema deve marcar o CHECK de entidade em cada tabela")
    if _MARCA_CENTRO not in sql:
        raise RuntimeError("schema deve marcar o centro padrao da EF")
    if CENTRO_EF in sql:
        raise RuntimeError("centro EF-OPEX precisa vir de config.entidades")
    return sql.replace(_MARCA_CHECK, check_entidade_sql()).replace(_MARCA_CENTRO, CENTRO_EF)
