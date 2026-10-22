"""gf-core: OS industrial, EF-OPEX, CNPJ, RNA, FK, caixa e CSV.

Coletado por `python -m pytest tests/` no workflow founder_panel_tests.yml.
Fixtures numéricas e de CNPJ são óbvias e não representam cadastro real.
"""

from __future__ import annotations

import csv
import io
import sqlite3
import sys
import zipfile
from datetime import date
from pathlib import Path

import pytest

APP_ROOT = Path(__file__).resolve().parents[1] / "apps" / "gf-core"
sys.path.insert(0, str(APP_ROOT))

from core.cnpj import normalizar_cnpj
from core.entities import CENTRO_EF, STATUS_INICIAL_OS, STATUS_OS, TIPOS_EQUIPAMENTO
from core.errors import (
    CnpjError,
    EntityIsolationError,
    IntegrityFailure,
    NotFoundError,
    RnaAtlasError,
    TransitionError,
    ValidationError,
)
from core.export_bi import (
    COLUNAS_CENTROS,
    COLUNAS_CONSOLIDADO,
    COLUNAS_HEROS,
    csv_centros,
)
from core.rna_atlas import gerar_caminho, validar_caminho
from db.connection import connect
from db.repository import GfRepository

DIA = date(2026, 10, 22)
CNPJ_EF = "11.222.333/0001-81"
CNPJ_HC = "22.333.444/0001-81"
CNPJ_FSE = "33.444.555/0001-81"
CNPJ_AI = "44.555.666/0001-81"
VALOR_FIXTURE = 1.0
CADEIA = ["Orçamento", "Aprovado", "Em Manutenção", "Teste de Carga", "Faturado"]


@pytest.fixture
def repo(tmp_path: Path) -> GfRepository:
    return GfRepository(tmp_path / "grupo_fidalgo.db")


def _cadeia(
    repo: GfRepository,
    *,
    entidade: str,
    cnpj: str,
    serie: str,
    valor_final: float = 0.0,
    valor_orcamento: float = 0.0,
    centro: str | None = None,
    descricao: str = "Reparo fixture",
    tipo: str = "Transformador",
) -> tuple[dict, dict, dict]:
    cliente = repo.criar_cliente(
        entidade=entidade,
        razao_social=f"FIXTURE {entidade} LTDA",
        cnpj=cnpj,
        endereco="ENDERECO FIXTURE",
        email_fiscal="fiscal.fixture@example.invalid",
    )
    equipamento = repo.criar_equipamento(
        entidade=entidade,
        id_cliente=cliente["id_cliente"],
        tipo_equipamento=tipo,
        numero_serie=serie,
        marca_modelo="MARCA FIXTURE",
        potencia_especificacao="FIXTURE",
        quando=DIA,
    )
    ordem = repo.abrir_os(
        entidade=entidade,
        id_cliente=cliente["id_cliente"],
        id_equipamento=equipamento["id_equipamento"],
        data_abertura=DIA,
        descricao_servico=descricao,
        valor_orcamento=valor_orcamento,
        valor_final=valor_final,
        centro_custo=centro,
        responsavel_tecnico="TECNICO FIXTURE",
    )
    return cliente, equipamento, ordem


def _faturar(repo: GfRepository, ordem: dict) -> dict:
    atual = ordem
    for destino in CADEIA[1:]:
        atual = repo.transicionar_os(atual["id_os"], destino, entidade=atual["entidade"], quando=DIA)
    return atual


def test_cnpj_fixture_valido_e_mascara():
    assert normalizar_cnpj(CNPJ_EF) == "11222333000181"
    assert normalizar_cnpj("11222333000181") == "11222333000181"
    assert normalizar_cnpj(CNPJ_HC) == "22333444000181"


@pytest.mark.parametrize(
    "bruto",
    [
        "11.111.111/1111-11",
        "11.111.111/1111-80",
        "00.000.000/0000-00",
        "11.222.333/0001-80",
        "123",
        "abcdef",
        "",
        "11.222.333/0001-81abc",
    ],
)
def test_cnpj_invalido(bruto: str):
    with pytest.raises(CnpjError):
        normalizar_cnpj(bruto)


def test_rna_exemplo_founder_incremento_e_recusas():
    assert validar_caminho("20261022_EF_Laudo_Transformador_Pesa_V01.pdf").versao == 1
    primeiro = gerar_caminho("EF", "Laudo Transformador Pesa", "pdf", quando=DIA, existentes=[])
    assert primeiro == "20261022_EF_Laudo_Transformador_Pesa_V01.pdf"
    segundo = gerar_caminho("EF", "Laudo Transformador Pesa", "pdf", quando=DIA, existentes=[primeiro])
    assert segundo == "20261022_EF_Laudo_Transformador_Pesa_V02.pdf"
    decimo = gerar_caminho(
        "EF",
        "Laudo Transformador Pesa",
        "pdf",
        quando=DIA,
        existentes=["20261022_EF_Laudo_Transformador_Pesa_V09.pdf"],
    )
    assert decimo.endswith("_V10.pdf")
    with pytest.raises(RnaAtlasError):
        gerar_caminho(
            "EF",
            "Laudo Transformador Pesa",
            "pdf",
            quando=DIA,
            existentes=["20261022_EF_Laudo_Transformador_Pesa_V99.pdf"],
        )
    with pytest.raises(RnaAtlasError):
        validar_caminho("20261015_AI_Relatorio_Locacao_Outubro.pdf")
    with pytest.raises(RnaAtlasError):
        validar_caminho("20261022_FS_Proposta_Manutencao_V01.docx")
    with pytest.raises(RnaAtlasError):
        validar_caminho("20261022_EF_Laudo_Transformador_Pesa_V00.pdf")
    with pytest.raises(RnaAtlasError):
        validar_caminho("20260231_EF_Laudo_Transformador_Pesa_V01.pdf")
    with pytest.raises(RnaAtlasError):
        validar_caminho("../20261022_EF_Laudo_Transformador_Pesa_V01.pdf")


def test_fluxo_os_industrial_ate_faturado(repo: GfRepository):
    assert list(TIPOS_EQUIPAMENTO) == ["Transformador", "Motor Elétrico", "Gerador", "Disjuntor"]
    assert STATUS_INICIAL_OS == "Orçamento"
    assert list(STATUS_OS) == CADEIA
    _cliente, equipamento, ordem = _cadeia(repo, entidade="EF", cnpj=CNPJ_EF, serie="SN-FIXTURE-EF-01")
    assert equipamento["status_atual"] == "Diagnóstico"
    assert equipamento["link_pasta_drive"] == "20261022_EF_Pasta_Transformador_V01.dir"
    assert ordem["status_os"] == "Orçamento"
    assert ordem["centro_custo"] == CENTRO_EF
    assert ordem["valor_orcamento"] == 0.0
    assert ordem["valor_final"] == 0.0
    assert ordem["data_conclusao"] is None
    atual = ordem
    for destino in CADEIA[1:]:
        atual = repo.transicionar_os(atual["id_os"], destino, entidade="EF", quando=DIA)
        assert atual["status_os"] == destino
        assert atual["centro_custo"] == CENTRO_EF
        if destino != "Faturado":
            assert atual["data_conclusao"] is None
    assert atual["status_os"] == "Faturado"
    assert atual["data_conclusao"] == "2026-10-22"
    with pytest.raises(TransitionError):
        repo.transicionar_os(atual["id_os"], "Aprovado", entidade="EF", quando=DIA)


def test_transicao_nao_pula_etapa(repo: GfRepository):
    _cliente, _equipamento, ordem = _cadeia(
        repo, entidade="EF", cnpj=CNPJ_EF, serie="SN-FIXTURE-EF-02"
    )
    with pytest.raises(TransitionError):
        repo.transicionar_os(ordem["id_os"], "Faturado", entidade="EF", quando=DIA)
    assert repo.obter_os(ordem["id_os"], entidade="EF")["status_os"] == "Orçamento"


def test_ef_opex_obrigatorio_e_nao_vaza(repo: GfRepository):
    with pytest.raises(EntityIsolationError):
        _cadeia(
            repo,
            entidade="EF",
            cnpj=CNPJ_EF,
            serie="SN-FIXTURE-EF-03",
            centro="FSE-OPEX",
        )
    cliente, equipamento, ordem = _cadeia(
        repo, entidade="FSE", cnpj=CNPJ_FSE, serie="SN-FIXTURE-FSE-01"
    )
    assert ordem["centro_custo"] == "FSE-OPEX"
    assert ordem["centro_custo"] != CENTRO_EF
    capex = repo.abrir_os(
        entidade="FSE",
        id_cliente=cliente["id_cliente"],
        id_equipamento=equipamento["id_equipamento"],
        data_abertura=DIA,
        centro_custo="FSE-CAPEX",
    )
    assert capex["centro_custo"] == "FSE-CAPEX"
    with pytest.raises(EntityIsolationError):
        repo.abrir_os(
            entidade="FSE",
            id_cliente=cliente["id_cliente"],
            id_equipamento=equipamento["id_equipamento"],
            data_abertura=DIA,
            centro_custo=CENTRO_EF,
        )


def test_default_sql_ef_opex_nao_entra_em_hc(repo: GfRepository):
    _cliente_ef, equipamento_ef, _ordem = _cadeia(
        repo, entidade="EF", cnpj=CNPJ_EF, serie="SN-FIXTURE-EF-04"
    )
    cliente_hc, equipamento_hc, ordem_hc = _cadeia(
        repo, entidade="HC", cnpj=CNPJ_HC, serie="SN-FIXTURE-HC-01"
    )
    assert ordem_hc["centro_custo"] == "HC-OPEX"
    conn = connect(repo.db_path)
    try:
        assert int(conn.execute("PRAGMA foreign_keys").fetchone()[0]) == 1
        conn.execute(
            """
            INSERT INTO ordens_servico (id_os, id_cliente, id_equipamento, entidade, data_abertura)
            VALUES ('OS-RAW-EF', ?, ?, 'EF', '2026-10-22')
            """,
            (equipamento_ef["id_cliente"], equipamento_ef["id_equipamento"]),
        )
        gravada = conn.execute(
            "SELECT status_os, centro_custo FROM ordens_servico WHERE id_os = 'OS-RAW-EF'"
        ).fetchone()
        assert gravada["status_os"] == "Orçamento"
        assert gravada["centro_custo"] == "EF-OPEX"
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO ordens_servico (id_os, id_cliente, id_equipamento, entidade, data_abertura)
                VALUES ('OS-RAW-HC', ?, ?, 'HC', '2026-10-22')
                """,
                (cliente_hc["id_cliente"], equipamento_hc["id_equipamento"]),
            )
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO ordens_servico (
                    id_os, id_cliente, id_equipamento, entidade, data_abertura, status_os, centro_custo
                ) VALUES ('OS-RAW-FAT', ?, ?, 'EF', '2026-10-22', 'Faturado', 'EF-OPEX')
                """,
                (equipamento_ef["id_cliente"], equipamento_ef["id_equipamento"]),
            )
    finally:
        conn.close()


def test_fk_cliente_inexistente_e_serie_repetida(repo: GfRepository):
    assert repo.foreign_keys_ativas() == 1
    with pytest.raises(NotFoundError):
        repo.criar_equipamento(
            entidade="EF",
            id_cliente="CLI-NAO-EXISTE",
            tipo_equipamento="Transformador",
            numero_serie="SN-FIXTURE-EF-05",
            quando=DIA,
        )
    conn = connect(repo.db_path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO equipamentos (
                    id_equipamento, id_cliente, entidade, tipo_equipamento, numero_serie, link_pasta_drive
                ) VALUES ('EQ-ORF', 'CLI-NAO-EXISTE', 'EF', 'Transformador', 'SN-ORF', '20261022_EF_Pasta_Transformador_V01.dir')
                """
            )
    finally:
        conn.close()
    _cliente, _equipamento, _ordem = _cadeia(
        repo, entidade="EF", cnpj=CNPJ_EF, serie="SN-FIXTURE-EF-06"
    )
    with pytest.raises(IntegrityFailure):
        repo.criar_cliente(entidade="HC", razao_social="FIXTURE HC LTDA", cnpj=CNPJ_EF)
    with pytest.raises(IntegrityFailure):
        repo.criar_equipamento(
            entidade="EF",
            id_cliente=_cliente["id_cliente"],
            tipo_equipamento="Gerador",
            numero_serie="SN-FIXTURE-EF-06",
            quando=DIA,
        )


def test_tipo_invalido_e_cnpj_nao_grava(repo: GfRepository):
    with pytest.raises(ValidationError):
        repo.criar_equipamento(
            entidade="EF",
            id_cliente="CLI-EF-0001",
            tipo_equipamento="Turbina",
            numero_serie="SN-FIXTURE-EF-07",
            quando=DIA,
        )
    with pytest.raises(CnpjError):
        repo.criar_cliente(entidade="EF", razao_social="FIXTURE EF LTDA", cnpj="00.000.000/0000-00")
    assert repo.listar_clientes("EF") == []


def test_link_pasta_incrementa_e_motor(repo: GfRepository):
    cliente, primeiro, _ordem = _cadeia(
        repo,
        entidade="EF",
        cnpj=CNPJ_EF,
        serie="SN-FIXTURE-EF-08",
        tipo="Motor Elétrico",
    )
    assert primeiro["link_pasta_drive"] == "20261022_EF_Pasta_Motor_Eletrico_V01.dir"
    segundo = repo.criar_equipamento(
        entidade="EF",
        id_cliente=cliente["id_cliente"],
        tipo_equipamento="Motor Elétrico",
        numero_serie="SN-FIXTURE-EF-09",
        quando=DIA,
    )
    assert segundo["link_pasta_drive"] == "20261022_EF_Pasta_Motor_Eletrico_V02.dir"


def test_isolamento_de_caixa_e_colunas_csv(repo: GfRepository):
    _ef_cli, _ef_eq, ef = _cadeia(
        repo,
        entidade="EF",
        cnpj=CNPJ_EF,
        serie="SN-FIXTURE-EF-10",
        valor_final=VALOR_FIXTURE,
        descricao="Reparo fixture, fase A",
    )
    _hc_cli, _hc_eq, hc = _cadeia(
        repo,
        entidade="HC",
        cnpj=CNPJ_HC,
        serie="SN-FIXTURE-HC-02",
        valor_final=VALOR_FIXTURE,
    )
    fse_cli, fse_eq, fse = _cadeia(
        repo,
        entidade="FSE",
        cnpj=CNPJ_FSE,
        serie="SN-FIXTURE-FSE-02",
        valor_final=VALOR_FIXTURE,
    )
    aberta = repo.abrir_os(
        entidade="EF",
        id_cliente=ef["id_cliente"],
        id_equipamento=ef["id_equipamento"],
        data_abertura=DIA,
        descricao_servico="Ainda orcamento",
        valor_orcamento=VALOR_FIXTURE,
        valor_final=VALOR_FIXTURE,
    )
    ef = _faturar(repo, ef)
    hc = _faturar(repo, hc)
    fse = _faturar(repo, fse)
    assert aberta["status_os"] == "Orçamento"

    with pytest.raises(NotFoundError) as vazou:
        repo.obter_os(ef["id_os"], entidade="HC")
    assert ef["descricao_servico"] not in str(vazou.value)
    assert repo.listar_os("EF")
    assert all(linha["entidade"] == "EF" for linha in repo.listar_os("EF"))
    assert hc["id_os"] not in {linha["id_os"] for linha in repo.listar_os("EF")}

    ef_csv = repo.exportar_csv_centros("EF")
    fse_csv = repo.exportar_csv_centros("FSE")
    with pytest.raises(EntityIsolationError):
        repo.exportar_csv_centros("HC")
    with pytest.raises(EntityIsolationError):
        repo.exportar_csv_heros("EF")

    ef_linhas = list(csv.DictReader(io.StringIO(ef_csv)))
    fse_linhas = list(csv.DictReader(io.StringIO(fse_csv)))
    assert list(csv.DictReader(io.StringIO(ef_csv)).fieldnames) == list(COLUNAS_CENTROS)
    assert ef_csv.startswith(",".join(COLUNAS_CENTROS) + "\n")
    assert len(ef_linhas) == 1
    assert ef_linhas[0]["Entidade"] == "EF"
    assert ef_linhas[0]["CentroCusto"] == "OPEX"
    assert ef_linhas[0]["AnoMes"] == "2026-10"
    assert ef_linhas[0]["Valor_R"] == "1.00"
    assert ef_linhas[0]["Cliente_Projeto"] == ef["id_cliente"]
    assert ef_linhas[0]["NF"] == ""
    assert "centro_custo=EF-OPEX" in ef_linhas[0]["Observacoes"]
    assert "separar_de=FSE" in ef_linhas[0]["Observacoes"]
    assert ef_linhas[0]["Descricao"] == "Reparo fixture, fase A"
    assert "FSE-OPEX" not in ef_csv
    assert hc["id_os"] not in ef_csv
    assert fse["id_os"] not in ef_csv
    assert aberta["id_os"] not in ef_csv
    assert fse_linhas[0]["Entidade"] == "FSE"
    assert fse_linhas[0]["CentroCusto"] == "OPEX"
    assert "centro_custo=FSE-OPEX" in fse_linhas[0]["Observacoes"]
    assert "EF-OPEX" not in fse_csv

    heros = repo.exportar_csv_heros("HC")
    heros_linhas = list(csv.DictReader(io.StringIO(heros)))
    assert list(csv.DictReader(io.StringIO(heros)).fieldnames) == list(COLUNAS_HEROS)
    assert len(heros_linhas) == 1
    assert heros_linhas[0]["Entidade"] == "HC"
    assert heros_linhas[0]["Tipo"] == "OS"
    assert heros_linhas[0]["Valor_R"] == "1.00"
    assert heros_linhas[0]["Qtd_OS"] == "1"
    assert heros_linhas[0]["Custo_R"] == ""
    assert heros_linhas[0]["Qtd_Vendas"] == ""
    assert ef["id_os"] not in heros

    grupo = repo.exportar_csv_consolidado("EF")
    grupo_linhas = list(csv.DictReader(io.StringIO(grupo)))
    assert list(csv.DictReader(io.StringIO(grupo)).fieldnames) == list(COLUNAS_CONSOLIDADO)
    assert len(grupo_linhas) == 1
    assert grupo_linhas[0]["Entidade"] == "EF"
    assert grupo_linhas[0]["Receita_R"] == "1.00"
    assert grupo_linhas[0]["Custo_R"] == ""
    assert grupo_linhas[0]["Resultado_R"] == ""
    assert grupo_linhas[0]["Patrimonio_Mercado_R"] == ""
    assert "3400000" not in grupo
    assert "617000" not in grupo
    vazio = repo.exportar_csv_consolidado("EF", anomes="2020-01")
    assert vazio.splitlines() == [",".join(COLUNAS_CONSOLIDADO)]
    with pytest.raises(ValidationError):
        repo.exportar_csv_consolidado("EF", anomes="2026-13")

    mistura = [dict(ef), dict(hc)]
    with pytest.raises(EntityIsolationError):
        csv_centros("EF", mistura)

    assert fse_cli and fse_eq


def test_backup_zip_rna(repo: GfRepository, tmp_path: Path):
    _cadeia(repo, entidade="AI", cnpj=CNPJ_AI, serie="SN-FIXTURE-AI-01")
    destino = tmp_path / "backups"
    primeiro = repo.criar_backup(destino, tag="EF", quando=DIA)
    assert primeiro.name == "20261022_EF_Backup_SQLite_V01.zip"
    validar_caminho(primeiro.name)
    with zipfile.ZipFile(primeiro) as pacote:
        assert pacote.namelist() == ["grupo_fidalgo.db"]
        info = pacote.getinfo("grupo_fidalgo.db")
        assert info.compress_type == zipfile.ZIP_DEFLATED
        assert pacote.read("grupo_fidalgo.db").startswith(b"SQLite format 3\x00")
    segundo = repo.criar_backup(destino, tag="EF", quando=DIA)
    assert segundo.name.endswith("_V02.zip")


def test_readme_contrato_e_arvore_sem_dado_real():
    readme = (APP_ROOT / "README.md").read_text(encoding="utf-8")
    requirements = (APP_ROOT / "requirements.txt").read_text(encoding="utf-8")
    schema = (APP_ROOT / "db" / "schema.sql").read_text(encoding="utf-8")
    assert "Grupo_Fidalgo_BI" in readme
    assert "3_FSE_CentrosCusto" in readme
    assert "2_Heros_Operacional" in readme
    assert "5_Grupo_Consolidado" in readme
    assert ",".join(COLUNAS_CENTROS) in readme
    assert ",".join(COLUNAS_HEROS) in readme
    assert ",".join(COLUNAS_CONSOLIDADO) in readme
    assert "EF-OPEX" in readme
    assert "foreign_keys" in readme
    assert "uvicorn api.app:app" in readme
    assert "streamlit run ui/streamlit_app.py" in readme
    assert "tests/test_gf_core.py" in readme
    assert "fastapi" in requirements
    assert "pydantic" in requirements
    assert "streamlit" in requirements
    assert "uvicorn" in requirements
    assert "PRAGMA foreign_keys = ON" in schema
    for pasta in ("api", "db", "ui", "core"):
        assert (APP_ROOT / pasta).is_dir()
    proibidos = ("hotmart.com", "n8n.io", "webhook", "31.402.321", "31402321000146", "bonaville", "3400000", "617000")
    for caminho in APP_ROOT.rglob("*"):
        if not caminho.is_file() or caminho.suffix not in {".py", ".md", ".sql", ".txt"}:
            continue
        texto = caminho.read_text(encoding="utf-8").lower()
        for token in proibidos:
            assert token not in texto, f"{token} em {caminho}"


def test_api_fluxo_local_se_fastapi(tmp_path: Path):
    pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.app import create_app

    client = TestClient(create_app(tmp_path / "api.db", backup_dir=tmp_path / "bkp"))
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["publicado"] is False
    assert health.json()["hotmart"] is False
    cliente = client.post(
        "/clientes",
        json={"entidade": "EF", "razao_social": "FIXTURE EF LTDA", "cnpj": CNPJ_EF},
    )
    assert cliente.status_code == 200, cliente.text
    id_cliente = cliente.json()["id_cliente"]
    equipamento = client.post(
        "/equipamentos",
        json={
            "entidade": "EF",
            "id_cliente": id_cliente,
            "tipo_equipamento": "Disjuntor",
            "numero_serie": "SN-FIXTURE-EF-11",
            "data_referencia": "2026-10-22",
        },
    )
    assert equipamento.status_code == 200, equipamento.text
    assert equipamento.json()["link_pasta_drive"] == "20261022_EF_Pasta_Disjuntor_V01.dir"
    ordem = client.post(
        "/ordens",
        json={
            "entidade": "EF",
            "id_cliente": id_cliente,
            "id_equipamento": equipamento.json()["id_equipamento"],
            "data_abertura": "2026-10-22",
            "centro_custo": "FSE-OPEX",
        },
    )
    assert ordem.status_code == 409
    ordem_ok = client.post(
        "/ordens",
        json={
            "entidade": "EF",
            "id_cliente": id_cliente,
            "id_equipamento": equipamento.json()["id_equipamento"],
            "data_abertura": "2026-10-22",
        },
    )
    assert ordem_ok.status_code == 200
    assert ordem_ok.json()["centro_custo"] == "EF-OPEX"
    id_os = ordem_ok.json()["id_os"]
    for destino in CADEIA[1:]:
        passo = client.post(
            f"/ordens/{id_os}/transicao",
            params={"entidade": "EF"},
            json={"status_destino": destino, "quando": "2026-10-22"},
        )
        assert passo.status_code == 200, passo.text
        assert passo.json()["status_os"] == destino
    alheia = client.get(f"/ordens/{id_os}", params={"entidade": "HC"})
    assert alheia.status_code == 404
    assert "FIXTURE" not in alheia.text
    lista = client.get("/ordens", params={"entidade": "EF"})
    assert lista.status_code == 200
    assert all(item["entidade"] == "EF" for item in lista.json()["itens"])
    csv_resp = client.get("/export/centros.csv", params={"entidade": "EF"})
    assert csv_resp.status_code == 200
    assert csv_resp.text.startswith(",".join(COLUNAS_CENTROS) + "\n")
    backup = client.post("/backup", json={"tag": "EF", "quando": "2026-10-22"})
    assert backup.status_code == 200
    assert backup.json()["nome"] == "20261022_EF_Backup_SQLite_V01.zip"
