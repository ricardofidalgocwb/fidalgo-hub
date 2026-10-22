"""CSV no contrato de colunas da planilha Grupo_Fidalgo_BI.

Cada arquivo sai de uma entidade só. Cabeçalhos iguais aos das abas;
células de custo e patrimônio que este app não apura ficam vazias.
"""

from __future__ import annotations

import csv
import io
import re

from core.entities import CENTRO_EF, validar_entidade
from core.errors import EntityIsolationError, ValidationError

PLANILHA = "Grupo_Fidalgo_BI"
ABA_CENTROS = "3_FSE_CentrosCusto"
ABA_HEROS = "2_Heros_Operacional"
ABA_CONSOLIDADO = "5_Grupo_Consolidado"

COLUNAS_CENTROS: tuple[str, ...] = (
    "AnoMes",
    "Entidade",
    "CentroCusto",
    "Descricao",
    "Valor_R",
    "Cliente_Projeto",
    "NF",
    "Observacoes",
)

COLUNAS_HEROS: tuple[str, ...] = (
    "AnoMes",
    "Entidade",
    "Tipo",
    "Categoria",
    "Valor_R",
    "Custo_R",
    "Margem_R",
    "Qtd_OS",
    "Qtd_Vendas",
    "Ocupacao_Vagas_pct",
    "Vagas_Inadimplentes",
    "Observacoes",
)

COLUNAS_CONSOLIDADO: tuple[str, ...] = (
    "AnoMes",
    "Entidade",
    "Receita_R",
    "Custo_R",
    "Resultado_R",
    "Patrimonio_Mercado_R",
    "Observacoes",
)

_OBS_HEROS = "gf-core local; somente OS Faturado HC"
_OBS_CONSOLIDADO = "gf-core local; receita=soma valor_final OS Faturado; custo e patrimonio em branco"


def validar_anomes(valor: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}", valor or ""):
        raise ValidationError("AnoMes invalido")
    mes = int(valor[5:7])
    if mes < 1 or mes > 12:
        raise ValidationError("AnoMes invalido")
    return valor


def centro_planilha(entidade: str, centro_custo: str) -> str:
    if entidade == "EF":
        if centro_custo != CENTRO_EF:
            raise EntityIsolationError("EF exige centro_custo EF-OPEX")
        return "OPEX"
    if entidade == "FSE":
        if centro_custo == "FSE-OPEX":
            return "OPEX"
        if centro_custo == "FSE-CAPEX":
            return "CAPEX"
        raise EntityIsolationError("centro FSE invalido para a aba 3_FSE_CentrosCusto")
    raise EntityIsolationError("aba 3_FSE_CentrosCusto nao recebe esta entidade")


def _ano_mes(iso_data: str) -> str:
    if not iso_data or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso_data):
        raise ValidationError("OS faturada sem data_conclusao")
    return validar_anomes(iso_data[:7])


def _dinheiro(valor: float) -> str:
    return f"{round(float(valor), 2):.2f}"


def _celula(valor: str | None) -> str:
    if not valor:
        return ""
    return " ".join(str(valor).split())


def _exigir_entidade(entidade: str, linhas: list[dict]) -> str:
    tag = validar_entidade(entidade)
    for linha in linhas:
        if linha.get("entidade") != tag:
            raise EntityIsolationError("vazamento de entidade no export")
        if linha.get("status_os") not in (None, "Faturado"):
            raise EntityIsolationError("export de caixa so aceita OS Faturado")
    return tag


def _escrever(colunas: tuple[str, ...], linhas: list[dict[str, str]]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(colunas), lineterminator="\n")
    writer.writeheader()
    for linha in linhas:
        writer.writerow(linha)
    return buffer.getvalue()


def _agrupar(entidade: str, linhas: list[dict], anomes: str | None) -> dict[str, list[dict]]:
    filtro = validar_anomes(anomes) if anomes else None
    grupos: dict[str, list[dict]] = {}
    for linha in linhas:
        competencia = _ano_mes(linha["data_conclusao"])
        if filtro and competencia != filtro:
            continue
        if linha["entidade"] != entidade:
            raise EntityIsolationError("vazamento de entidade no export")
        grupos.setdefault(competencia, []).append(linha)
    return dict(sorted(grupos.items()))


def csv_centros(entidade: str, linhas: list[dict]) -> str:
    tag = _exigir_entidade(entidade, linhas)
    if tag not in ("EF", "FSE"):
        raise EntityIsolationError("aba 3_FSE_CentrosCusto nao recebe esta entidade")
    saida: list[dict[str, str]] = []
    for linha in linhas:
        centro_interno = linha["centro_custo"]
        observacoes = f"id_os={linha['id_os']}; centro_custo={centro_interno}"
        if tag == "EF":
            observacoes += "; separar_de=FSE"
        saida.append(
            {
                "AnoMes": _ano_mes(linha["data_conclusao"]),
                "Entidade": tag,
                "CentroCusto": centro_planilha(tag, centro_interno),
                "Descricao": _celula(linha.get("descricao_servico")) or "OS",
                "Valor_R": _dinheiro(linha["valor_final"]),
                "Cliente_Projeto": linha["id_cliente"],
                "NF": "",
                "Observacoes": observacoes,
            }
        )
    return _escrever(COLUNAS_CENTROS, saida)


def csv_heros(entidade: str, linhas: list[dict]) -> str:
    tag = _exigir_entidade(entidade, linhas)
    if tag != "HC":
        raise EntityIsolationError("aba 2_Heros_Operacional so recebe HC")
    saida: list[dict[str, str]] = []
    for competencia, itens in _agrupar(tag, linhas, None).items():
        for item in itens:
            if item["centro_custo"] != "HC-OPEX":
                raise EntityIsolationError("caixa HC fora de HC-OPEX")
        saida.append(
            {
                "AnoMes": competencia,
                "Entidade": "HC",
                "Tipo": "OS",
                "Categoria": "Servicos",
                "Valor_R": _dinheiro(sum(item["valor_final"] for item in itens)),
                "Custo_R": "",
                "Margem_R": "",
                "Qtd_OS": str(len(itens)),
                "Qtd_Vendas": "",
                "Ocupacao_Vagas_pct": "",
                "Vagas_Inadimplentes": "",
                "Observacoes": _OBS_HEROS,
            }
        )
    return _escrever(COLUNAS_HEROS, saida)


def csv_consolidado(entidade: str, linhas: list[dict], anomes: str | None = None) -> str:
    tag = _exigir_entidade(entidade, linhas)
    saida: list[dict[str, str]] = []
    for competencia, itens in _agrupar(tag, linhas, anomes).items():
        saida.append(
            {
                "AnoMes": competencia,
                "Entidade": tag,
                "Receita_R": _dinheiro(sum(item["valor_final"] for item in itens)),
                "Custo_R": "",
                "Resultado_R": "",
                "Patrimonio_Mercado_R": "",
                "Observacoes": _OBS_CONSOLIDADO,
            }
        )
    return _escrever(COLUNAS_CONSOLIDADO, saida)
