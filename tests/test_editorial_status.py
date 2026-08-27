"""Testes da máquina de status da Fila Editorial."""

from __future__ import annotations

import pytest

from editorial.status_machine import (
    ACTION_ADIAR,
    ACTION_APROVAR,
    ACTION_NOVO,
    ACTION_PUBLICAR,
    ACTION_RECUSAR,
    CANAL_NAO_PUBLICAR,
    MIN_RECUSA_REASON,
    PROP_AUTOMACAO,
    PROP_CANAL,
    PROP_OBSERVACOES,
    PROP_PROXIMA,
    PROP_STATUS,
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
    STATUS_PUBLICADO,
    STATUS_RASCUNHO,
    STATUS_RECUSADO,
    TransitionError,
    assert_canal_nao_publicar_on_create,
    assert_editorial_only_payload,
    assert_never_automacao_true,
    assert_never_publicado,
    build_transition,
    publish_allowed_for_action,
)


def test_aprovar_rascunho_para_aprovado():
    t = build_transition(ACTION_APROVAR, STATUS_RASCUNHO)
    assert t.to_status == STATUS_APROVADO
    assert t.properties[PROP_STATUS]["select"]["name"] == STATUS_APROVADO
    assert t.fire_n8n is False
    assert t.fire_instagram is False
    assert t.fire_site is False
    assert_editorial_only_payload(t.properties)
    assert_never_publicado(t.properties)
    assert PROP_CANAL not in t.properties
    assert PROP_AUTOMACAO not in t.properties


def test_aprovar_aguardando_ok_para_aprovado():
    t = build_transition(ACTION_APROVAR, STATUS_AGUARDANDO)
    assert t.to_status == STATUS_APROVADO
    assert t.fire_instagram is False
    assert t.fire_n8n is False


@pytest.mark.parametrize("status", [STATUS_APROVADO, STATUS_PUBLICADO, STATUS_RECUSADO])
def test_aprovar_status_invalido(status):
    with pytest.raises(TransitionError):
        build_transition(ACTION_APROVAR, status)


def test_aprovar_nunca_vira_publicado():
    t = build_transition(ACTION_APROVAR, STATUS_AGUARDANDO)
    assert t.to_status != STATUS_PUBLICADO
    with pytest.raises(TransitionError, match="Founder"):
        assert_never_publicado({PROP_STATUS: {"select": {"name": STATUS_PUBLICADO}}})


def test_acao_publicar_nao_existe():
    with pytest.raises(TransitionError, match="não publica"):
        build_transition(ACTION_PUBLICAR, STATUS_APROVADO)
    assert publish_allowed_for_action(ACTION_APROVAR) is False
    assert publish_allowed_for_action(ACTION_PUBLICAR) is False
    assert publish_allowed_for_action(ACTION_RECUSAR) is False
    assert publish_allowed_for_action(ACTION_ADIAR) is False


def test_recusar_exige_motivo():
    with pytest.raises(TransitionError, match="motivo"):
        build_transition(ACTION_RECUSAR, STATUS_AGUARDANDO, reason="não")
    with pytest.raises(TransitionError):
        build_transition(ACTION_RECUSAR, STATUS_RASCUNHO, reason=None)


def test_recusar_grava_recusado():
    reason = "mito 12V 1967 no texto"
    assert len(reason) >= MIN_RECUSA_REASON
    t = build_transition(ACTION_RECUSAR, STATUS_RASCUNHO, reason=reason)
    assert t.to_status == STATUS_RECUSADO
    assert t.fire_n8n is False
    assert t.fire_instagram is False
    text = t.properties[PROP_OBSERVACOES]["rich_text"][0]["text"]["content"]
    assert "Recusa Mesa" in text
    assert reason in text


def test_adiar_volta_rascunho_sem_inventar_adiado():
    t = build_transition(ACTION_ADIAR, STATUS_AGUARDANDO, reason="esperar grid")
    assert t.to_status == STATUS_RASCUNHO
    assert t.to_status != "Adiado"
    assert t.fire_instagram is False
    assert PROP_PROXIMA in t.properties
    assert "Adiado Mesa" in t.properties[PROP_OBSERVACOES]["rich_text"][0]["text"]["content"]


def test_adiar_de_aprovado_tambem_volta_rascunho():
    t = build_transition(ACTION_ADIAR, STATUS_APROVADO)
    assert t.to_status == STATUS_RASCUNHO
    assert t.fire_site is False


def test_nao_mexe_em_publicado():
    with pytest.raises(TransitionError, match="já Publicado"):
        build_transition(ACTION_ADIAR, STATUS_PUBLICADO)
    with pytest.raises(TransitionError, match="já Publicado"):
        build_transition(ACTION_RECUSAR, STATUS_PUBLICADO, reason="motivo longo ok")


def test_novo_card_canal_nao_publicar():
    t = build_transition(
        ACTION_NOVO,
        None,
        peca="EDI · Ficha teste",
        braco="Editora",
        formato="Ficha",
    )
    assert t.to_status == STATUS_RASCUNHO
    assert t.properties[PROP_CANAL]["select"]["name"] == CANAL_NAO_PUBLICAR
    assert t.properties[PROP_AUTOMACAO]["checkbox"] is False
    assert t.fire_instagram is False
    assert_canal_nao_publicar_on_create(t.properties)
    assert_never_automacao_true(t.properties)
    assert_editorial_only_payload(t.properties, creating=True)


def test_novo_recusa_sem_peca():
    with pytest.raises(TransitionError, match="Peça"):
        build_transition(ACTION_NOVO, None, braco="Editora", formato="Ficha")


def test_proibe_agt09():
    from editorial.status_machine import assert_not_forbidden_agent

    with pytest.raises(TransitionError, match="AGT-09"):
        assert_not_forbidden_agent("AGT-09")


def test_ids_ssot_unico():
    from editorial.ids import FILA_EDITORIAL_DATA_SOURCE_ID, FILA_EDITORIAL_ID, fila_editorial

    cfg = fila_editorial()
    assert cfg["database_id"] == FILA_EDITORIAL_ID
    assert cfg["data_source_id"] == FILA_EDITORIAL_DATA_SOURCE_ID
    assert cfg["canal_default"] == "Não publicar"
    assert cfg["agents"]["Editora"] == "Acervo"
    assert cfg["agents"]["Produtora"] == "Comunicação"
    assert "AGT-09" in cfg["forbidden_agents"]


def test_payload_nao_escreve_propriedade_alheia():
    with pytest.raises(TransitionError, match="fora"):
        assert_editorial_only_payload({"Instagram": {"url": "x"}})
