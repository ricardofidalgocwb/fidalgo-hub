"""Nomes RNA Atlas: AAAAMMDD_TAG_DESCRICAO_Vxx.ext

A versão começa em V01 e sobe até V99 para a mesma data, tag, descrição e
extensão. A tag vem de config.entidades.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from config.entidades import ENTIDADES
from core.errors import RnaAtlasError

TAGS_RNA = "|".join(ENTIDADES)
_RNA = re.compile(
    rf"^(?P<data>\d{{8}})_(?P<tag>{TAGS_RNA})_"
    rf"(?P<descricao>[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z][A-Za-z0-9]*)*)_"
    rf"V(?P<versao>\d{{2}})\.(?P<ext>[A-Za-z0-9]{{1,8}})$"
)


@dataclass(frozen=True)
class RnaNome:
    data: date
    tag: str
    descricao: str
    versao: int
    ext: str
    nome: str


def normalizar_descricao(texto: str) -> str:
    if texto is None or not str(texto).strip():
        raise RnaAtlasError("descricao RNA vazia")
    sem_acento = unicodedata.normalize("NFKD", str(texto))
    sem_acento = "".join(char for char in sem_acento if not unicodedata.combining(char))
    partes: list[str] = []
    for bruto in re.split(r"[^A-Za-z0-9]+", sem_acento):
        token = re.sub(r"^[0-9]+", "", bruto)
        if token:
            partes.append(token)
    if not partes:
        raise RnaAtlasError("descricao RNA vazia")
    return "_".join(partes)


def _extensao(ext: str) -> str:
    limpa = str(ext).strip().lstrip(".").lower()
    if not re.fullmatch(r"[a-z0-9]{1,8}", limpa):
        raise RnaAtlasError("extensao RNA invalida")
    return limpa


def _data_rna(yyyymmdd: str) -> date:
    try:
        return date(int(yyyymmdd[0:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:8]))
    except ValueError as exc:
        raise RnaAtlasError("data RNA invalida") from exc


def validar_caminho(caminho: str) -> RnaNome:
    nome = "" if caminho is None else str(caminho).strip()
    if not nome or nome != Path(nome).name or "/" in nome or "\\" in nome:
        raise RnaAtlasError("caminho RNA deve ser um unico segmento")
    encontrado = _RNA.fullmatch(nome)
    if not encontrado:
        raise RnaAtlasError("caminho fora do padrao AAAAMMDD_TAG_DESCRICAO_Vxx.ext")
    versao = int(encontrado.group("versao"))
    if versao < 1:
        raise RnaAtlasError("versao RNA comeca em V01")
    tag = encontrado.group("tag")
    if tag not in ENTIDADES:
        raise RnaAtlasError("tag RNA desconhecida")
    return RnaNome(
        data=_data_rna(encontrado.group("data")),
        tag=tag,
        descricao=encontrado.group("descricao"),
        versao=versao,
        ext=encontrado.group("ext"),
        nome=nome,
    )


def gerar_caminho(
    tag: str,
    descricao: str,
    ext: str,
    *,
    quando: date | None = None,
    existentes: list[str] | tuple[str, ...] = (),
) -> str:
    if tag not in ENTIDADES:
        raise RnaAtlasError("tag RNA desconhecida")
    descricao_norm = normalizar_descricao(descricao)
    extensao = _extensao(ext)
    dia = quando or date.today()
    versoes: list[int] = []
    for item in existentes:
        try:
            atual = validar_caminho(Path(str(item)).name)
        except RnaAtlasError:
            continue
        if (
            atual.data == dia
            and atual.tag == tag
            and atual.descricao == descricao_norm
            and atual.ext.lower() == extensao
        ):
            versoes.append(atual.versao)
    proxima = (max(versoes) if versoes else 0) + 1
    if proxima > 99:
        raise RnaAtlasError("versao RNA excede V99")
    nome = f"{dia.strftime('%Y%m%d')}_{tag}_{descricao_norm}_V{proxima:02d}.{extensao}"
    validar_caminho(nome)
    return nome
