"""Preço lançado pelo operador. Zero não é preço."""

from __future__ import annotations

from core.errors import ValidationError


def interpretar_preco(valor: float | str | None, campo: str) -> float | None:
    """None, vazio ou 0 viram sem preço (NULL). Não inventa valor."""
    if valor is None:
        return None
    if isinstance(valor, str):
        bruto = valor.strip().replace(",", ".")
        if not bruto:
            return None
        valor = bruto
    try:
        numero = round(float(valor), 2)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{campo} invalido") from exc
    if numero < 0:
        raise ValidationError(f"{campo} negativo")
    if numero == 0:
        return None
    return numero


def interpretar_recebido(valor: float | str | None) -> float:
    numero = interpretar_preco(valor, "valor_recebido")
    if numero is None:
        raise ValidationError("valor_recebido obrigatorio")
    return numero


def texto_preco(valor: float | None) -> str:
    """Exportação: sem preço sai célula vazia, nunca 0.00."""
    numero = interpretar_preco(valor, "valor")
    if numero is None:
        return ""
    return f"{numero:.2f}"


def soma_precos(valores: list[float | None]) -> str:
    total = 0.0
    tem_preco = False
    for valor in valores:
        numero = interpretar_preco(valor, "valor")
        if numero is None:
            continue
        total += numero
        tem_preco = True
    if not tem_preco:
        return ""
    return f"{round(total, 2):.2f}"
