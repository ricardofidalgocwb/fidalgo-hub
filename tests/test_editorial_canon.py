"""Canon da mesa: 12V=1968, fim BR=1996, NAP 439, sem volume inventado."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dashboard.editorial_canon import (
    CANON_12V_YEAR,
    CANON_ANCHIETA_NACIONAL,
    CANON_ANCHIETA_PLANTA,
    CANON_FIM_BR_YEAR,
    CANON_IPIRANGA_CKD,
    CANON_ITAMAR,
    CANON_MEXICO_YEAR,
    assert_card_canon,
    canon_summary,
    scan_card,
)
from dashboard.editorial_runner import EditorialClient, build_dry_run_report, main
from dashboard.editorial_status import (
    ACTION_APROVAR,
    STATUS_AGUARDANDO,
    STATUS_RASCUNHO,
    EditorialError,
    build_transition,
)


def test_fatos_travados_nao_inventados():
    summary = canon_summary()
    assert summary["12v"] == 1968 == CANON_12V_YEAR
    assert summary["12v_implica_alternador"] is False
    assert summary["fim_br"] == 1996 == CANON_FIM_BR_YEAR
    assert summary["mexico"] == 2003 == CANON_MEXICO_YEAR
    assert summary["anchieta_nacional"] == "03/01/1959" == CANON_ANCHIETA_NACIONAL
    assert summary["anchieta_planta"] == "18/11/1959" == CANON_ANCHIETA_PLANTA
    assert CANON_IPIRANGA_CKD == 2268
    assert CANON_ITAMAR == 47700
    assert summary["volumes"] == [2268, 47700]


def test_metrica_canonica_passa():
    issues = scan_card(metrica="12 V = 1968; fim BR = 1996; NAP 439")
    assert issues == []


def test_metrica_viva_kit_datar_passa():
    issues = scan_card(metrica="12 V = 1968; fim BR = 1996; sem mito 2003")
    assert issues == []


def test_sem_os_viva_nao_e_os_viva():
    issues = scan_card(metrica="Pilar história 25% · 1 CTA só · sem OS viva")
    assert issues == []


def test_rejeita_12v_1967():
    issues = scan_card(metrica="12V=1967 no chicote")
    assert any(i.code == "myth_12v_1967" for i in issues)


def test_12v_nao_implica_alternador():
    issues = scan_card(metrica="12 V implica alternador em 1968")
    assert any(i.code == "myth_12v_alternator" for i in issues)
    ok = scan_card(metrica="12 V = 1968; 12 V não implica alternador")
    assert not any(i.code == "myth_12v_alternator" for i in ok)


def test_rejeita_fim_br_2003():
    issues = scan_card(metrica="fim BR=2003")
    assert any(i.code == "myth_fim_br_2003" for i in issues)


def test_mexico_2003_nao_e_mito():
    issues = scan_card(metrica="México = 2003 (não é fim BR)")
    assert not any(i.code == "myth_fim_br_2003" for i in issues)


def test_anchieta_datas_canônicas_passam():
    issues = scan_card(
        peca="EDI · Reel histórico (Anchieta 1959)",
        metrica="nacional 03/01/1959; planta 18/11/1959",
    )
    assert not any(i.code == "myth_anchieta" for i in issues)


def test_rejeita_anchieta_ano_errado():
    issues = scan_card(peca="Reel Anchieta 1958")
    assert any(i.code == "myth_anchieta" for i in issues)


def test_rejeita_anchieta_datas_trocadas():
    issues = scan_card(metrica="Anchieta nacional 18/11/1959")
    assert any(i.code == "myth_anchieta" for i in issues)


def test_rejeita_cpf():
    issues = scan_card(observacoes="cliente 123.456.789-00")
    assert any(i.code == "cpf" for i in issues)


def test_rejeita_os_viva_identificada():
    issues = scan_card(peca="Post OS-01 Willian")
    assert any(i.code == "os_viva" for i in issues)
    issues2 = scan_card(metrica="HC-2026-011 no ar")
    assert any(i.code == "os_viva" for i in issues2)


def test_rejeita_volume_inventado():
    issues = scan_card(metrica="produção 900000 unidades")
    assert any(i.code == "volume_inventado" for i in issues)
    issues_ok = scan_card(metrica="CKD Ipiranga 2268 Sedan · Itamar 47700")
    assert not any(i.code == "volume_inventado" for i in issues_ok)


def test_rejeita_dois_milhoes_inventados():
    issues = scan_card(metrica="2 milhões de fuscas no BR")
    assert any(i.code == "volume_inventado" for i in issues)


def test_figura_fora_do_canon_nao_passa_em_silencio():
    issues = scan_card(metrica="produção 150000")
    assert any(i.code == "volume_inventado" for i in issues)
    assert_card_canon(metrica="Itamar 47700 · Ipiranga 2268")


def test_aprovar_bloqueia_mito():
    with pytest.raises(EditorialError, match="Canon recusado"):
        build_transition(
            ACTION_APROVAR,
            STATUS_AGUARDANDO,
            metrica="12V=1967 e fim BR=2003",
        )


def test_aprovar_bloqueia_volume_inventado():
    with pytest.raises(EditorialError, match="volume"):
        build_transition(
            ACTION_APROVAR,
            STATUS_RASCUNHO,
            peca="EDI · Almanaque",
            metrica="2 milhões de fuscas no BR",
        )


def test_apply_action_recusa_mito_sem_escrever():
    mock_client = MagicMock()
    runner = EditorialClient(client=mock_client)
    with pytest.raises(EditorialError, match="Canon recusado"):
        runner.apply_action(
            "page-mito",
            ACTION_APROVAR,
            STATUS_RASCUNHO,
            metrica="12V=1967",
            printer=lambda _m: None,
        )
    mock_client.pages.update.assert_not_called()


def test_dry_run_report_separa_canon_bloqueado():
    cards = [
        {
            "id": "ok",
            "codigo": "EDI-1",
            "peca": "Kit Datar",
            "status": STATUS_RASCUNHO,
            "canal": "Não publicar",
            "metrica": "12 V = 1968; fim BR = 1996",
            "observacoes": "",
            "proxima_acao": "",
        },
        {
            "id": "bad",
            "codigo": "EDI-9",
            "peca": "Volume inflado",
            "status": STATUS_RASCUNHO,
            "canal": "Não publicar",
            "metrica": "2 milhões de fuscas no BR",
            "observacoes": "",
            "proxima_acao": "",
        },
    ]
    report = build_dry_run_report(cards, "teste")
    assert len(report["planned"]) == 1
    assert report["planned"][0]["peca"] == "Kit Datar"
    assert len(report["canon_blocked"]) == 1
    assert report["canon_blocked"][0]["codigo"] == "EDI-9"
    assert report["canon_blocked"][0]["canon_issues"][0]["code"] == "volume_inventado"
    assert report["written"] is False
    assert report["publish"] is False


def test_cli_approve_mito_falha(capsys):
    with patch("dashboard.editorial_runner.load_cards") as load:
        load.return_value = (
            [
                {
                    "id": "page-mito",
                    "codigo": "EDI-9",
                    "peca": "Mito",
                    "status": STATUS_RASCUNHO,
                    "canal": "Não publicar",
                    "metrica": "12V=1967",
                    "observacoes": "",
                    "proxima_acao": "",
                }
            ],
            "teste",
        )
        rc = main(["--approve", "EDI-9"])
    assert rc == 1
    err = capsys.readouterr().err
    assert "Canon recusado" in err
