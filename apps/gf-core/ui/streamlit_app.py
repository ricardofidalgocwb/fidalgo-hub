"""Painel local. streamlit run executa este arquivo; não importe de outro módulo."""

from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import streamlit as st

from core.entities import (
    CENTRO_EF,
    CENTROS_POR_ENTIDADE,
    ENTIDADES,
    NOME_ENTIDADE,
    STATUS_OS,
    TIPOS_EQUIPAMENTO,
    proximos_status,
)
from core.errors import GfCoreError
from db.connection import default_db_path
from db.repository import GfRepository


def _repo() -> GfRepository:
    return GfRepository(Path(st.session_state["db_path"]))


def _chamar(acao):
    try:
        return True, acao()
    except GfCoreError as exc:
        st.error(f"{type(exc).__name__}: {exc}")
        return False, None


def _tabela(linhas: list[dict], vazio: str) -> None:
    if not linhas:
        st.info(vazio)
        return
    st.dataframe(linhas, width="stretch", hide_index=True)


def _aba_clientes(entidade: str) -> None:
    st.subheader("Clientes B2B")
    repo = _repo()
    _tabela(repo.listar_clientes(entidade), "Nenhum cliente nesta entidade.")
    with st.form("cliente"):
        razao = st.text_input("Razão social")
        cnpj = st.text_input("CNPJ")
        contato = st.text_input("Contato responsável")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail fiscal")
        endereco = st.text_input("Endereço")
        obs = st.text_area("Observações")
        if st.form_submit_button("Salvar cliente"):
            ok, criado = _chamar(
                lambda: repo.criar_cliente(
                    entidade=entidade,
                    razao_social=razao,
                    cnpj=cnpj,
                    contato_responsavel=contato,
                    telefone=telefone,
                    email_fiscal=email,
                    endereco=endereco,
                    observacoes=obs,
                )
            )
            if ok:
                st.success(f"Cliente {criado['id_cliente']} gravado em {entidade}.")
                st.rerun()


def _aba_equipamentos(entidade: str) -> None:
    st.subheader("Equipamentos")
    repo = _repo()
    clientes = repo.listar_clientes(entidade)
    _tabela(repo.listar_equipamentos(entidade), "Nenhum equipamento nesta entidade.")
    if not clientes:
        st.info("Cadastre um cliente desta entidade antes do equipamento.")
        return
    with st.form("equipamento"):
        cliente = st.selectbox(
            "Cliente",
            clientes,
            format_func=lambda item: f"{item['id_cliente']} · {item['razao_social']}",
        )
        tipo = st.selectbox("Tipo", TIPOS_EQUIPAMENTO)
        serie = st.text_input("Número de série")
        marca = st.text_input("Marca / modelo")
        potencia = st.text_input("Potência / especificação")
        if st.form_submit_button("Salvar equipamento"):
            ok, criado = _chamar(
                lambda: repo.criar_equipamento(
                    entidade=entidade,
                    id_cliente=cliente["id_cliente"],
                    tipo_equipamento=tipo,
                    numero_serie=serie,
                    marca_modelo=marca,
                    potencia_especificacao=potencia,
                )
            )
            if ok:
                st.success(f"Pasta RNA: {criado['link_pasta_drive']}")
                st.rerun()


def _aba_ordens(entidade: str) -> None:
    st.subheader("Ordens de serviço")
    repo = _repo()
    status = st.selectbox("Filtrar status", ["Todos", *STATUS_OS])
    linhas = repo.listar_os(entidade, None if status == "Todos" else status)
    _tabela(linhas, "Nenhuma OS nesta entidade.")
    clientes = repo.listar_clientes(entidade)
    if clientes:
        cliente = st.selectbox(
            "Cliente da OS",
            clientes,
            format_func=lambda item: f"{item['id_cliente']} · {item['razao_social']}",
        )
        equipamentos = repo.listar_equipamentos(entidade, cliente["id_cliente"])
        if equipamentos:
            with st.form("os"):
                equipamento = st.selectbox(
                    "Equipamento",
                    equipamentos,
                    format_func=lambda item: f"{item['id_equipamento']} · {item['numero_serie']}",
                )
                descricao = st.text_area("Descrição do serviço")
                abertura = st.date_input("Data de abertura")
                informar_previsao = st.checkbox("Informar previsão")
                previsao = st.date_input("Previsão") if informar_previsao else None
                valor_orcamento = st.number_input("Valor orçamento (lançamento local)", min_value=0.0, value=0.0, step=0.01)
                valor_final = st.number_input("Valor final (lançamento local)", min_value=0.0, value=0.0, step=0.01)
                responsavel = st.text_input("Responsável técnico")
                centros = CENTROS_POR_ENTIDADE[entidade]
                if entidade == "EF":
                    st.text_input("Centro de custo", value=CENTRO_EF, disabled=True)
                    centro = CENTRO_EF
                else:
                    centro = st.selectbox("Centro de custo", centros)
                if st.form_submit_button("Abrir OS"):
                    ok, criada = _chamar(
                        lambda: repo.abrir_os(
                            entidade=entidade,
                            id_cliente=cliente["id_cliente"],
                            id_equipamento=equipamento["id_equipamento"],
                            data_abertura=abertura,
                            data_previsao=previsao,
                            descricao_servico=descricao,
                            valor_orcamento=valor_orcamento,
                            valor_final=valor_final,
                            centro_custo=centro,
                            responsavel_tecnico=responsavel,
                        )
                    )
                    if ok:
                        st.success(f"OS {criada['id_os']} em {criada['status_os']} · {criada['centro_custo']}")
                        st.rerun()
        else:
            st.info("Este cliente ainda não tem equipamento nesta entidade.")
    else:
        st.info("Cadastre um cliente desta entidade antes da OS.")

    abertas = [linha for linha in repo.listar_os(entidade) if proximos_status(linha["status_os"])]
    if not abertas:
        return
    escolhida = st.selectbox(
        "OS para transicionar",
        abertas,
        format_func=lambda item: f"{item['id_os']} · {item['status_os']}",
    )
    destino = st.selectbox("Próximo status", proximos_status(escolhida["status_os"]))
    if st.button("Aplicar transição"):
        ok, atualizada = _chamar(
            lambda: repo.transicionar_os(escolhida["id_os"], destino, entidade=entidade)
        )
        if ok:
            st.success(f"{atualizada['id_os']} agora está {atualizada['status_os']}.")
            st.rerun()


def _aba_exportar(entidade: str) -> None:
    st.subheader("Exportação Grupo_Fidalgo_BI")
    st.caption("Um arquivo, uma entidade. O app não escreve na planilha.")
    repo = _repo()
    if entidade in ("EF", "FSE"):
        csv_centros = repo.exportar_csv_centros(entidade)
        st.download_button(
            "Baixar 3_FSE_CentrosCusto",
            data=csv_centros.encode("utf-8"),
            file_name=f"{entidade}_3_FSE_CentrosCusto.csv",
            mime="text/csv",
        )
    elif entidade == "HC":
        csv_heros = repo.exportar_csv_heros(entidade)
        st.download_button(
            "Baixar 2_Heros_Operacional",
            data=csv_heros.encode("utf-8"),
            file_name="HC_2_Heros_Operacional.csv",
            mime="text/csv",
        )
    else:
        st.info("AI e PF saem só no consolidado. A aba de centros da FSE não recebe essas entidades.")
    csv_grupo = repo.exportar_csv_consolidado(entidade)
    st.download_button(
        "Baixar 5_Grupo_Consolidado",
        data=csv_grupo.encode("utf-8"),
        file_name=f"{entidade}_5_Grupo_Consolidado.csv",
        mime="text/csv",
    )


def main() -> None:
    st.set_page_config(page_title="gf-core local", layout="wide")
    st.title("gf-core · Holding Grupo Fidalgo")
    st.caption("Local e unpublished. Sem dados reais, sem n8n, sem Hotmart, sem publicação.")
    if "db_path" not in st.session_state:
        st.session_state["db_path"] = str(default_db_path())
    with st.sidebar:
        entidade = st.selectbox("Entidade", ENTIDADES, format_func=lambda tag: f"{tag} · {NOME_ENTIDADE[tag]}")
        st.session_state["db_path"] = st.text_input("SQLite local", value=st.session_state["db_path"])
        st.caption("Centro fixo da EF: EF-OPEX. Caixa de outra entidade não entra nesta tela.")
        if st.button("Gerar backup zip"):
            ok, arquivo = _chamar(lambda: _repo().criar_backup(APP_ROOT / "backups", tag=entidade))
            if ok:
                st.success(arquivo.name)
    crm, equipamentos, ordens, exportar = st.tabs(["CRM", "Equipamentos", "Ordens", "Exportar"])
    with crm:
        _aba_clientes(entidade)
    with equipamentos:
        _aba_equipamentos(entidade)
    with ordens:
        _aba_ordens(entidade)
    with exportar:
        _aba_exportar(entidade)


if __name__ == "__main__":
    main()
