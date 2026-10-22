"""Referência de foto tipada informada pelo operador. O app não cria o arquivo."""

from __future__ import annotations

import re
from pathlib import Path

from core.errors import ValidationError

_MARCADORES = frozenset(
    {
        "n/a",
        "na",
        "tbd",
        "todo",
        "default",
        "teste",
        "test",
        "xxx",
        "placeholder",
        "sem foto",
        "fake",
    }
)


def texto_obrigatorio(valor: str | None, campo: str) -> str:
    texto = "" if valor is None else str(valor).strip()
    if not texto or texto.casefold() in _MARCADORES:
        raise ValidationError(f"{campo} obrigatorio")
    return texto


def validar_ref_tipada(valor: str | None) -> str:
    texto = texto_obrigatorio(valor, "ref_foto_tipada")
    if texto.lower().startswith(("http://", "https://")):
        raise ValidationError("referencia de foto tipada deve ser caminho ou id")
    if any(parte == ".." for parte in texto.replace("\\", "/").split("/")):
        raise ValidationError("referencia de foto tipada invalida")
    if re.fullmatch(r"[A-Za-z0-9_-]{20,}", texto):
        return texto
    nome = Path(texto).name
    if "." not in nome or nome.startswith(".") or nome.endswith("."):
        raise ValidationError("referencia de foto tipada invalida")
    return texto.replace("\\", "/")
