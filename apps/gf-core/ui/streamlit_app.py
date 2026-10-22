"""Painel local. streamlit run executa este arquivo; não importe de outro módulo."""

from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import streamlit as st

from core.entities import CENTRO_EF, CENTROS_POR_ENTIDADE, ENTIDADES, STATUS_OS, TIPOS_EQUIPAMENTO, proximos_status
from core.errors import GfCoreError, ValidationError
from core.preco import interpretar_preco
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


def _preco_form(texto: str, campo: str):
    try:
        return interpretar_preco(texto, campo)
    except ValidationError:
        raise
    except ValueError as exc:
        raise ValidationError(f"{campo} invalido") from exc


def _exibir_os(linhas: list[dict]) -> list[dict]:
    saida = []
    for linha in linhas:
        item = dict(linha)
        for campo in ("valor_orcamento", "valor_final"):
            if item.get(campo) is None:
                item[campo] = "sem preço"
        saida.append(item)
    return saida


def _tabela(linhas: list[dict], vazio: str) -> None:
    if not linhas:
        st.info(vazio)
        return
    st.dataframe(linhas, width="stretch", hide_index=True)


def _aba_clientes(entidade: str) -> None:
    st.subheader("Clientes")
    repo = _repo()
    _tabela(repo.listar_clientes(entidade), "Nenhum cliente nesta entidade.")
    with st.form("cliente"):
        razao = st.text_input("Razão social")
        cnpj = st.text_input("CNPJ")
        contato = st.text_input("Contato")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")
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
                st.success(f"Cliente {criado['id_cliente']} gravado.")
                st.rerun()


def _aba_equipamentos(entidade: str) -> None:
    st.subheader("Equipamentos")
    st.caption("O número de série é digitado. O app não gera série.")
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
            ok, _criado = _chamar(
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
                st.success("Equipamento gravado.")
                st.rerun()


def _aba_ordens(entidade: str) -> None:
    st.subheader("Ordens de serviço")
    st.caption("Campo vazio ou zero em valor fica sem preço. Faturado não lança recebimento.")
    repo = _repo()
    status = st.selectbox("Filtrar status", ["Todos", *STATUS_OS])
    linhas = repo.listar_os(entidade, None if status == "Todos" else status)
    _tabela(_exibir_os(linhas), "Nenhuma OS nesta entidade.")
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
                valor_orcamento = st.text_input("Valor orçamento")
                valor_final = st.text_input("Valor final")
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
                            valor_orcamento=_preco_form(valor_orcamento, "valor_orcamento"),
                            valor_final=_preco_form(valor_final, "valor_final"),
                            centro_custo=centro,
                            responsavel_tecnico=responsavel,
                        )
                    )
                    if ok:
                        st.success(f"OS {criada['id_os']} · pasta {criada['link_pasta_drive']}")
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
    if destino in ("Teste de Carga", "Faturado"):
        st.caption("Esta passagem exige medição registrada e referência de foto tipada.")
    if st.button("Aplicar transição"):
        ok, atualizada = _chamar(
            lambda: repo.transicionar_os(escolhida["id_os"], destino, entidade=entidade)
        )
        if ok:
            st.success(f"{atualizada['id_os']} agora está {atualizada['status_os']}.")
            st.rerun()


def _aba_evidencia(entidade: str) -> None:
    st.subheader("Medição e foto tipada")
    st.caption("Sem valor padrão. A referência da foto é um caminho ou id informado aqui.")
    repo = _repo()
    _tabela(repo.listar_medicoes(entidade), "Nenhuma medição nesta entidade.")
    ordens = repo.listar_os(entidade)
    if not ordens:
        st.info("Nenhuma OS nesta entidade.")
        return
    ordem = st.selectbox(
        "OS",
        ordens,
        format_func=lambda item: f"{item['id_os']} · {item['status_os']}",
    )
    with st.form("medicao"):
        grandeza = st.text_input("Grandeza")
        valor = st.text_input("Valor medido")
        unidade = st.text_input("Unidade")
        dia = st.date_input("Data da medição")
        responsavel = st.text_input("Responsável pela medição")
        if st.form_submit_button("Registrar medição"):
            ok, _med = _chamar(
                lambda: repo.registrar_medicao(
                    entidade=entidade,
                    id_os=ordem["id_os"],
                    grandeza=grandeza,
                    valor=valor,
                    unidade=unidade,
                    data=dia,
                    responsavel=responsavel,
                )
            )
            if ok:
                st.success("Medição registrada.")
                st.rerun()
    with st.form("foto"):
        referencia = st.text_input("Caminho ou id da foto tipada")
        if st.form_submit_button("Registrar foto tipada"):
            ok, _os = _chamar(
                lambda: repo.registrar_foto_tipada(ordem["id_os"], entidade=entidade, referencia=referencia)
            )
            if ok:
                st.success("Referência registrada.")
                st.rerun()


def _aba_recebimentos(entidade: str) -> None:
    st.subheader("Recebimentos")
    st.caption("Faturado não cria recebimento. O lançamento é separado.")
    repo = _repo()
    _tabela(repo.listar_recebimentos(entidade), "Nenhum recebimento nesta entidade.")
    ordens = repo.listar_os(entidade)
    if not ordens:
        st.info("Nenhuma OS nesta entidade.")
        return
    with st.form("recebimento"):
        ordem = st.selectbox(
            "OS do recebimento",
            ordens,
            format_func=lambda item: f"{item['id_os']} · {item['status_os']}",
        )
        dia = st.date_input("Data do recebimento")
        valor = st.text_input("Valor recebido")
        forma = st.text_input("Forma")
        obs = st.text_input("Obs")
        if st.form_submit_button("Registrar recebimento"):
            ok, criado = _chamar(
                lambda: repo.registrar_recebimento(
                    entidade=entidade,
                    id_os=ordem["id_os"],
                    data_recebimento=dia,
                    valor_recebido=valor,
                    forma=forma,
                    obs=obs,
                )
            )
            if ok:
                st.success(f"Recebimento {criado['id']} registrado. Status da OS não muda.")
                st.rerun()


def _aba_exportar(entidade: str) -> None:
    st.subheader("Exportação")
    st.caption("Um arquivo, uma entidade. Sem preço sai célula vazia. O app não escreve na planilha.")
    repo = _repo()
    if entidade in ("EF", "FSE"):
        csv_centros = repo.exportar_csv_centros(entidade)
        st.download_button(
            "Baixar centros de custo",
            data=csv_centros.encode("utf-8"),
            file_name=f"{entidade}_centros_custo.csv",
            mime="text/csv",
        )
    elif entidade == "HC":
        csv_operacional = repo.exportar_csv_operacional(entidade)
        st.download_button(
            "Baixar operacional HC",
            data=csv_operacional.encode("utf-8"),
            file_name="HC_operacional.csv",
            mime="text/csv",
        )
    else:
        st.info("AI e PF saem só no consolidado.")
    csv_grupo = repo.exportar_csv_consolidado(entidade)
    st.download_button(
        "Baixar consolidado",
        data=csv_grupo.encode("utf-8"),
        file_name=f"{entidade}_consolidado.csv",
        mime="text/csv",
    )


def main() -> None:
    st.set_page_config(page_title="gf-core", layout="wide")
    st.title("gf-core")
    st.caption("Local. Unpublished. Sem dados reais.")
    if "db_path" not in st.session_state:
        st.session_state["db_path"] = str(default_db_path())
    with st.sidebar:
        entidade = st.selectbox("Entidade", ENTIDADES)
        st.session_state["db_path"] = st.text_input("SQLite local", value=st.session_state["db_path"])
        st.caption("EF usa o centro EF-OPEX. Cada tela mostra só a entidade escolhida.")
        if st.button("Gerar backup zip"):
            ok, arquivo = _chamar(lambda: _repo().criar_backup(APP_ROOT / "backups", tag=entidade))
            if ok:
                st.success(arquivo.name)
    abas = st.tabs(["Clientes", "Equipamentos", "Ordens", "Evidência", "Recebimentos", "Exportar"])
    with abas[0]:
        _aba_clientes(entidade)
    with abas[1]:
        _aba_equipamentos(entidade)
    with abas[2]:
        _aba_ordens(entidade)
    with abas[3]:
        _aba_evidencia(entidade)
    with abas[4]:
        _aba_recebimentos(entidade)
    with abas[5]:
        _aba_exportar(entidade)


if __name__ == "__main__":
    main()
