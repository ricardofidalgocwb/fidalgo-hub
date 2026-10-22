"""Validação de CNPJ pelos dígitos verificadores.

Não consulta a Receita e não traz cadastro real. Sequências com os 12
primeiros dígitos iguais (incluindo 00000000000000) são recusadas, mesmo
quando a conta do dígito fecharia.
"""

from __future__ import annotations

import re

from core.errors import CnpjError

_PESOS_1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_PESOS_2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_PONTUACAO = re.compile(r"^[\d.\-/\s]+$")


def _digito(numeros: str, pesos: tuple[int, ...]) -> str:
    soma = sum(int(numero) * peso for numero, peso in zip(numeros, pesos, strict=True))
    resto = soma % 11
    return "0" if resto < 2 else str(11 - resto)


def normalizar_cnpj(valor: str | None) -> str:
    if valor is None or not str(valor).strip():
        raise CnpjError("cnpj vazio")
    bruto = str(valor).strip()
    if not _PONTUACAO.fullmatch(bruto):
        raise CnpjError("cnpj invalido")
    digitos = re.sub(r"\D", "", bruto)
    if len(digitos) != 14 or len(set(digitos[:12])) == 1:
        raise CnpjError("cnpj invalido")
    esperado = _digito(digitos[:12], _PESOS_1)
    esperado += _digito(digitos[:12] + esperado, _PESOS_2)
    if digitos[12:] != esperado:
        raise CnpjError("cnpj invalido")
    return digitos
