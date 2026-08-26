"""Testes da máquina de status da Fila Founder."""

from __future__ import annotations

from datetime import date

import pytest

from dashboard.status_machine import (
    ACTION_ADIAR,
    ACTION_APROVAR,
    ACTION_AVANCAR,
    ACTION_RECUSAR,
    MIN_RECUSA_REASON,
    PROP_DATA_OK,
    PROP_OBSERVACOES,
    PROP_STATUS,
    STATUS_ADIADO,
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
    STATUS_CONCLUIDO,
    STATUS_EM_EXECUCAO,
    STATUS_REJEITADO,
    TransitionError,
    assert_fila_founder_only_payload,
    assert_not_archived_leads,
    assert_not_os_entregue_writer,
    build_transition,
    fila_sort_key,
    flags_heros_vs_fse,
    n8n_allowed_for_action,
)


TODAY = date(2026, 8, 26)


def test_aprovar_aguardando_ok_para_aprovado():
    t = build_transition(ACTION_APROVAR, STATUS_AGUARDANDO, today=TODAY)
    assert t.to_status == STATUS_APROVADO
    assert t.properties[PROP_STATUS]["select"]["name"] == STATUS_APROVADO
    assert t.properties[PROP_DATA_OK]["date"]["start"] == "2026-08-26"
    assert t.fire_n8n is False
    assert_fila_founder_only_payload(t.properties)


def test_aprovar_nunca_dispara_n8n_mesmo_com_flag():
    t = build_transition(
        ACTION_APROVAR, STATUS_AGUARDANDO, today=TODAY, n8n_avancar_enabled=True
    )
    assert t.fire_n8n is False
    assert n8n_allowed_for_action(ACTION_APROVAR, True) is False


@pytest.mark.parametrize("status", [STATUS_APROVADO, STATUS_EM_EXECUCAO, STATUS_CONCLUIDO])
def test_aprovar_status_invalido(status):
    with pytest.raises(TransitionError):
        build_transition(ACTION_APROVAR, status)


def test_avancar_aprovado_para_em_execucao_sem_n8n():
    t = build_transition(ACTION_AVANCAR, STATUS_APROVADO, n8n_avancar_enabled=False)
    assert t.to_status == STATUS_EM_EXECUCAO
    assert t.fire_n8n is False
    assert t.log_only is True
    assert PROP_DATA_OK not in t.properties


def test_avancar_pode_marcar_n8n_somente_com_flag():
    t = build_transition(ACTION_AVANCAR, STATUS_APROVADO, n8n_avancar_enabled=True)
    assert t.fire_n8n is True
    assert n8n_allowed_for_action(ACTION_AVANCAR, True) is True
    assert n8n_allowed_for_action(ACTION_AVANCAR, False) is False


def test_avancar_recusa_aguardando_ok():
    with pytest.raises(TransitionError, match="Avançar só vale"):
        build_transition(ACTION_AVANCAR, STATUS_AGUARDANDO)


def test_recusar_exige_motivo():
    with pytest.raises(TransitionError, match="motivo"):
        build_transition(ACTION_RECUSAR, STATUS_AGUARDANDO, reason="não")
    with pytest.raises(TransitionError):
        build_transition(ACTION_RECUSAR, STATUS_AGUARDANDO, reason=None)


def test_recusar_grava_rejeitado_e_observacao():
    reason = "risco L0 sem laudo"
    assert len(reason) >= MIN_RECUSA_REASON
    t = build_transition(ACTION_RECUSAR, STATUS_AGUARDANDO, reason=reason, today=TODAY)
    assert t.to_status == STATUS_REJEITADO
    assert t.fire_n8n is False
    text = t.properties[PROP_OBSERVACOES]["rich_text"][0]["text"]["content"]
    assert "Recusa Founder" in text
    assert reason in text


def test_adiar_para_adiado():
    t = build_transition(ACTION_ADIAR, STATUS_APROVADO, today=TODAY)
    assert t.to_status == STATUS_ADIADO
    assert t.fire_n8n is False


def test_n8n_nunca_em_recusar_nem_adiar():
    assert n8n_allowed_for_action(ACTION_RECUSAR, True) is False
    assert n8n_allowed_for_action(ACTION_ADIAR, True) is False


def test_l0_vem_antes_de_p0_e_caixa():
    l0 = fila_sort_key("1 · L0", "L0 Segurança", "Crítica")
    p0 = fila_sort_key("2 · P0/Crítica", "L1 Compliance", "Crítica")
    caixa = fila_sort_key("3 · Caixa", "L4 Caixa/Margem", "Alta")
    demais = fila_sort_key("4 · Demais", "L6 Interno", "Baixa")
    assert l0 < p0 < caixa < demais


def test_alerta_nao_misturar_fse_heros_na_caixa():
    msg = flags_heros_vs_fse(
        "Caixa Zero FSE",
        "CNPJ FSE separado da Heros Custom",
        "3 · Caixa",
    )
    assert msg
    assert "FSE" in msg


def test_proibido_leads_arquivado():
    with pytest.raises(TransitionError, match="43b3f514"):
        assert_not_archived_leads("43b3f514aaaaaaaaaaaaaaaaaaaaaaaa")


def test_proibido_escrever_os_entregue():
    from dashboard.ids import OS_DATABASE_ID

    with pytest.raises(TransitionError, match="OS"):
        assert_not_os_entregue_writer(
            OS_DATABASE_ID, {PROP_STATUS: {"select": {"name": "Aprovado"}}}
        )
    with pytest.raises(TransitionError, match="Entregue"):
        assert_not_os_entregue_writer(
            "01cb462a-0237-4aab-9ddc-1735d1e1ea23",
            {PROP_STATUS: {"select": {"name": "Entregue"}}, PROP_DATA_OK: {}},
        )
