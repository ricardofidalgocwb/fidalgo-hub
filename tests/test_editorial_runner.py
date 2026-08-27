"""Runner editorial: dry-run, Aprovar ≠ publicar, sem n8n, sem outras DBs."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dashboard.editorial_runner import (
    EditorialClient,
    build_dry_run_report,
    find_card,
    load_cards,
    main,
    writes_allowed,
)
from dashboard.editorial_status import (
    ACTION_APROVAR,
    ACTION_RECUSAR,
    CANAL_NAO_PUBLICAR,
    FORBIDDEN_DB_LABELS,
    MIN_RECUSA_REASON,
    PROP_CANAL,
    PROP_OBSERVACOES,
    PROP_STATUS,
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
    STATUS_PUBLICADO,
    STATUS_RASCUNHO,
    STATUS_RECUSADO,
    EditorialError,
    assert_editorial_database_only,
    assert_editorial_only_payload,
    assert_never_publicado,
    build_transition,
    n8n_allowed_for_editorial_action,
)
from dashboard.ids import (
    CLIENTES_ID,
    CRM_OPORTUNIDADES_ID,
    FILA_EDITORIAL_ID,
    FILA_FOUNDER_ID,
    FINANCEIRO_ID,
    OS_DATABASE_ID,
    fila_editorial,
    load_ids,
    runner_only_database_ids,
    writable_database_ids,
)

FIXTURE = Path(__file__).resolve().parent.parent / "dashboard" / "fixtures" / "sample_fila_editorial.json"
EDI1 = "3c97d36b-ae64-8126-a798-c1fc475bfaa7"
EDI2 = "3c97d36b-ae64-8153-afca-df4cc630baae"


def _last_json(text: str) -> dict:
    decoder = json.JSONDecoder()
    found = None
    idx = 0
    while True:
        pos = text.find("{", idx)
        if pos < 0:
            break
        try:
            found, end = decoder.raw_decode(text[pos:])
        except json.JSONDecodeError:
            idx = pos + 1
            continue
        idx = pos + end
    assert found is not None
    return found


def _queue():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_ids_editorial_write_false_runner_only():
    cfg = fila_editorial()
    assert cfg["database_id"] == FILA_EDITORIAL_ID
    assert cfg["data_source_id"] == "13be9ea3-a48d-464f-9c10-e15203c3a61a"
    assert cfg["write"] is False
    assert cfg["runner_only"] is True
    compact = FILA_EDITORIAL_ID.replace("-", "").lower()
    assert compact not in writable_database_ids()
    assert compact in runner_only_database_ids()
    assert FILA_FOUNDER_ID.replace("-", "").lower() in writable_database_ids()


def test_ids_schema_nao_inventa_propriedades():
    expected = {
        "Peça",
        "Nº",
        "Status",
        "Braço",
        "Canal",
        "Formato",
        "Porta",
        "Métrica",
        "Observações",
        "Próxima ação",
        "Data",
        "Automação executada",
    }
    assert set(fila_editorial()["properties"].values()) == expected
    assert load_ids()["editorial_rule"]
    assert "Aprovar" in load_ids()["editorial_rule"]


def test_fixture_lista_edi1_edi2_sem_inventar():
    cards = _queue()
    assert [c["codigo"] for c in cards] == ["EDI-1", "EDI-2"]
    datar = cards[0]
    anchieta = cards[1]
    assert datar["peca"] == "EDI · Kit Datar (M0 D1)"
    assert datar["id"] == EDI1
    assert datar["status"] == STATUS_RASCUNHO
    assert datar["canal"] == CANAL_NAO_PUBLICAR
    assert datar["braco"] == "Editora"
    assert datar["formato"] == "Ficha"
    assert "1968" in datar["metrica"]
    assert "1996" in datar["metrica"]
    assert anchieta["peca"] == "EDI · Reel histórico (Anchieta 1959)"
    assert anchieta["id"] == EDI2
    assert anchieta["status"] == STATUS_RASCUNHO
    assert anchieta["canal"] == CANAL_NAO_PUBLICAR
    assert anchieta["braco"] == "Produtora"
    assert anchieta["formato"] == "Reel"
    assert all(c["automacao_executada"] is False for c in cards)


def test_dry_run_report_planeja_aprovado_e_nao_publicado():
    report = build_dry_run_report(_queue(), "fixture")
    assert report["dry_run"] is True
    assert report["written"] is False
    assert report["n8n_fired"] is False
    assert report["publish"] is False
    assert report["write"] is False
    assert len(report["planned"]) == 2
    for item in report["planned"]:
        assert item["to_status"] == STATUS_APROVADO
        assert item["from_status"] == STATUS_RASCUNHO
        assert item["properties"][PROP_STATUS]["select"]["name"] == STATUS_APROVADO
        assert PROP_CANAL not in item["properties"]
        assert item["canal_unchanged"] == CANAL_NAO_PUBLICAR
        assert item["fire_n8n"] is False
        assert item["publish"] is False
        assert item["to_status"] != STATUS_PUBLICADO
    pecas = {item["peca"] for item in report["planned"]}
    assert "EDI · Kit Datar (M0 D1)" in pecas
    assert "EDI · Reel histórico (Anchieta 1959)" in pecas


def test_cli_dry_run_lista_fila(capsys):
    rc = main(["--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "EDI · Kit Datar (M0 D1)" in out
    assert "EDI · Reel histórico (Anchieta 1959)" in out
    assert "EDI-1" in out
    assert "EDI-2" in out
    assert STATUS_APROVADO in out
    assert "Aprovar ≠ publicar" in out
    payload = _last_json(out)
    assert payload["written"] is False
    assert all(p["to_status"] != STATUS_PUBLICADO for p in payload["planned"])


def test_cli_sem_flags_tambem_e_dry_run(capsys):
    rc = main([])
    assert rc == 0
    out = capsys.readouterr().out
    payload = _last_json(out)
    assert payload["dry_run"] is True
    assert payload["written"] is False
    assert "Kit Datar" in out


def test_aprovar_rascunho_e_aguardando_ok():
    for status in (STATUS_RASCUNHO, STATUS_AGUARDANDO):
        t = build_transition(ACTION_APROVAR, status, canal=CANAL_NAO_PUBLICAR)
        assert t.to_status == STATUS_APROVADO
        assert t.properties[PROP_STATUS]["select"]["name"] == STATUS_APROVADO
        assert PROP_CANAL not in t.properties
        assert PROP_OBSERVACOES not in t.properties
        assert t.fire_n8n is False
        assert t.publish is False
        assert t.canal_unchanged == CANAL_NAO_PUBLICAR
        assert_editorial_only_payload(t.properties)
        assert_never_publicado(t.properties)


def test_aprovar_com_observacao_nao_muda_canal():
    t = build_transition(ACTION_APROVAR, STATUS_RASCUNHO, reason="ok mesa")
    assert PROP_OBSERVACOES in t.properties
    assert PROP_CANAL not in t.properties


@pytest.mark.parametrize("status", [STATUS_APROVADO, STATUS_PUBLICADO, STATUS_RECUSADO])
def test_aprovar_status_invalido(status):
    with pytest.raises(EditorialError):
        build_transition(ACTION_APROVAR, status)


def test_recusa_acao_publicar():
    with pytest.raises(EditorialError, match="recusa publicar"):
        build_transition("publicar", STATUS_APROVADO)
    with pytest.raises(EditorialError, match="recusa publicar"):
        build_transition("publish", STATUS_RASCUNHO)


def test_recusa_definir_publicado_no_payload():
    with pytest.raises(EditorialError, match="Publicado"):
        assert_never_publicado({PROP_STATUS: {"select": {"name": STATUS_PUBLICADO}}})
    with pytest.raises(EditorialError, match="Canal"):
        assert_never_publicado({PROP_CANAL: {"select": {"name": "IG"}}})


def test_n8n_nunca_no_editorial():
    assert n8n_allowed_for_editorial_action(ACTION_APROVAR) is False
    assert n8n_allowed_for_editorial_action(ACTION_RECUSAR) is False
    assert n8n_allowed_for_editorial_action("avancar") is False
    t = build_transition(ACTION_APROVAR, STATUS_RASCUNHO)
    assert t.fire_n8n is False


def test_recusar_grava_recusado():
    reason = "fora do tom da mesa"
    assert len(reason) >= MIN_RECUSA_REASON
    t = build_transition(ACTION_RECUSAR, STATUS_RASCUNHO, reason=reason)
    assert t.to_status == STATUS_RECUSADO
    assert t.fire_n8n is False
    assert t.publish is False
    text = t.properties[PROP_OBSERVACOES]["rich_text"][0]["text"]["content"]
    assert "Recusa editorial" in text


def test_recusar_exige_motivo():
    with pytest.raises(EditorialError, match="motivo"):
        build_transition(ACTION_RECUSAR, STATUS_RASCUNHO, reason="não")


@pytest.mark.parametrize(
    "database_id",
    [FILA_FOUNDER_ID, OS_DATABASE_ID, CRM_OPORTUNIDADES_ID, CLIENTES_ID, FINANCEIRO_ID],
)
def test_recusa_escrever_outras_databases(database_id):
    with pytest.raises(EditorialError, match="Fila Editorial"):
        assert_editorial_database_only(database_id)
    assert database_id in FORBIDDEN_DB_LABELS


def test_editorial_database_ok():
    assert_editorial_database_only(FILA_EDITORIAL_ID)
    assert_editorial_database_only(FILA_EDITORIAL_ID.replace("-", ""))


def test_payload_nao_pode_incluir_canal_ou_automacao():
    with pytest.raises(EditorialError):
        assert_editorial_only_payload(
            {
                PROP_STATUS: {"select": {"name": STATUS_APROVADO}},
                PROP_CANAL: {"select": {"name": "IG"}},
            }
        )
    with pytest.raises(EditorialError):
        assert_editorial_only_payload({"Automação executada": {"checkbox": True}})


def test_writes_allowed_exige_token_e_confirm():
    with patch("dashboard.editorial_runner.notion_token", return_value=None):
        with patch("dashboard.editorial_runner.confirm_env", return_value=True):
            assert writes_allowed() is False
    with patch("dashboard.editorial_runner.notion_token", return_value="ntn_test"):
        with patch("dashboard.editorial_runner.confirm_env", return_value=False):
            assert writes_allowed() is False
        with patch("dashboard.editorial_runner.confirm_env", return_value=True):
            assert writes_allowed() is True


def test_aprovar_dry_run_nao_chama_pages_update():
    mock_client = MagicMock()
    runner = EditorialClient(client=mock_client)
    with patch("dashboard.editorial_runner.writes_allowed", return_value=False):
        result = runner.apply_action(
            EDI1,
            ACTION_APROVAR,
            STATUS_RASCUNHO,
            canal=CANAL_NAO_PUBLICAR,
            printer=lambda _m: None,
        )
    mock_client.pages.update.assert_not_called()
    mock_client.databases.query.assert_not_called()
    assert result.dry_run is True
    assert result.written is False
    assert result.n8n_fired is False
    assert result.publish is False
    assert result.transition.to_status == STATUS_APROVADO
    assert PROP_CANAL not in result.payload["properties"]


def test_aprovar_confirm_so_status_aprovado():
    mock_client = MagicMock()
    runner = EditorialClient(client=mock_client)
    with patch("dashboard.editorial_runner.notion_token", return_value="ntn_test"):
        with patch("dashboard.editorial_runner.writes_allowed", return_value=True):
            result = runner.apply_action(
                EDI1,
                ACTION_APROVAR,
                STATUS_RASCUNHO,
                canal=CANAL_NAO_PUBLICAR,
                printer=lambda _m: None,
            )
    mock_client.pages.update.assert_called_once()
    kwargs = mock_client.pages.update.call_args.kwargs
    assert kwargs["page_id"] == EDI1
    assert kwargs["properties"][PROP_STATUS]["select"]["name"] == STATUS_APROVADO
    assert set(kwargs["properties"]) <= {PROP_STATUS, PROP_OBSERVACOES}
    assert PROP_CANAL not in kwargs["properties"]
    assert kwargs["properties"][PROP_STATUS]["select"]["name"] != STATUS_PUBLICADO
    assert result.n8n_fired is False
    assert result.publish is False
    assert result.written is True
    assert result.dry_run is False


def test_cli_approve_dry_run_sem_confirm(capsys):
    rc = main(["--approve", "EDI-1"])
    assert rc == 0
    out = capsys.readouterr().out
    data = _last_json(out)
    assert data["dry_run"] is True
    assert data["written"] is False
    assert data["n8n_fired"] is False
    assert data["publish"] is False
    assert data["to_status"] == STATUS_APROVADO
    assert data["payload"]["properties"][PROP_STATUS]["select"]["name"] == STATUS_APROVADO


def test_cli_refuse_sem_motivo_falha(capsys):
    rc = main(["--refuse", EDI2, "--reason", "não"])
    assert rc == 1
    err = capsys.readouterr().err
    assert "motivo" in err.lower()


def test_find_card_por_codigo():
    card = find_card(_queue(), "EDI-1")
    assert card is not None
    assert card["id"] == EDI1


def test_load_cards_sem_token_usa_fixture():
    with patch("dashboard.editorial_runner.notion_token", return_value=None):
        cards, source = load_cards()
    assert "NOTION_TOKEN" in source or "demonstração" in source
    assert len(cards) == 2


def test_normalize_unique_id_edi():
    from dashboard.editorial_runner import EditorialClient

    page = {
        "id": EDI1,
        "url": "https://www.notion.so/3c97d36bae648126a798c1fc475bfaa7",
        "properties": {
            "Peça": {"title": [{"plain_text": "EDI · Kit Datar (M0 D1)"}]},
            "Nº": {"unique_id": {"prefix": "EDI", "number": 1}},
            "Status": {"select": {"name": "Rascunho"}},
            "Braço": {"select": {"name": "Editora"}},
            "Canal": {"select": {"name": "Não publicar"}},
            "Formato": {"select": {"name": "Ficha"}},
            "Porta": {"select": {"name": "Venda"}},
            "Métrica": {"rich_text": [{"plain_text": "12 V = 1968; fim BR = 1996"}]},
            "Observações": {"rich_text": []},
            "Próxima ação": {"rich_text": []},
            "Data": {"date": None},
            "Automação executada": {"checkbox": False},
        },
    }
    card = EditorialClient(client=MagicMock())._normalize_page(page)
    assert card["codigo"] == "EDI-1"
    assert card["numero"] == 1
    assert card["canal"] == CANAL_NAO_PUBLICAR
    assert card["status"] == STATUS_RASCUNHO
    assert "1968" in card["metrica"]
    assert "1996" in card["metrica"]
