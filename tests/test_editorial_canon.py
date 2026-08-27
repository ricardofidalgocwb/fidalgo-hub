"""Canon da mesa: 12V=1968, fim BR=1996, NAP 439, sem volume inventado."""

from __future__ import annotations

import pytest

from editorial.canon import scan_card
from editorial.status_machine import (
    ACTION_APROVAR,
    ACTION_NOVO,
    STATUS_AGUARDANDO,
    TransitionError,
    build_transition,
)


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


def test_rejeita_fim_br_2003():
    issues = scan_card(metrica="fim BR=2003")
    assert any(i.code == "myth_fim_br_2003" for i in issues)


def test_mexico_2003_nao_e_mito():
    issues = scan_card(metrica="México = 2003 (não é fim BR)")
    assert not any(i.code == "myth_fim_br_2003" for i in issues)


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


def test_aprovar_bloqueia_mito():
    with pytest.raises(TransitionError, match="Canon recusado"):
        build_transition(
            ACTION_APROVAR,
            STATUS_AGUARDANDO,
            metrica="12V=1967 e fim BR=2003",
        )


def test_novo_bloqueia_volume_inventado():
    with pytest.raises(TransitionError, match="volume"):
        build_transition(
            ACTION_NOVO,
            None,
            peca="EDI · Almanaque",
            braco="Editora",
            formato="Almanaque",
            metrica="2 milhões de fuscas no BR",
        )
