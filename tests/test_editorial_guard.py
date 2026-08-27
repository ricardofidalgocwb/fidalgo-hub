"""Aprovar não publica: sem IG, sem n8n, sem Status Publicado, dry-run padrão."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from editorial.notion_fila import NotionEditorialClient, writes_allowed
from editorial.pulse import build_pulse
from editorial.status_machine import (
    ACTION_APROVAR,
    ACTION_NOVO,
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
)


def test_writes_allowed_sem_token():
    with patch("editorial.notion_fila.notion_token", return_value=None):
        with patch("editorial.notion_fila.confirm_env", return_value=True):
            assert writes_allowed() is False


def test_writes_allowed_token_sem_confirm():
    with patch("editorial.notion_fila.notion_token", return_value="ntn_test"):
        with patch("editorial.notion_fila.confirm_env", return_value=False):
            assert writes_allowed() is False


def test_writes_allowed_token_e_confirm():
    with patch("editorial.notion_fila.notion_token", return_value="ntn_test"):
        with patch("editorial.notion_fila.confirm_env", return_value=True):
            assert writes_allowed() is True


def test_aprovar_dry_run_nao_chama_pages_update():
    mock_client = MagicMock()
    fila = NotionEditorialClient(client=mock_client)
    with patch("editorial.notion_fila.writes_allowed", return_value=False):
        result = fila.apply_action(
            ACTION_APROVAR,
            page_id="page-1",
            current_status=STATUS_AGUARDANDO,
            printer=lambda _m: None,
        )
    mock_client.pages.update.assert_not_called()
    mock_client.pages.create.assert_not_called()
    assert result.dry_run is True
    assert result.written is False
    assert result.published is False
    assert result.n8n_fired is False
    assert result.instagram_posted is False
    assert result.transition.to_status == STATUS_APROVADO
    assert result.transition.fire_instagram is False
    assert result.transition.fire_n8n is False
    assert result.transition.fire_site is False


def test_aprovar_live_nao_posta_ig_nem_n8n():
    mock_client = MagicMock()
    fila = NotionEditorialClient(client=mock_client)
    with patch("editorial.notion_fila.writes_allowed", return_value=True):
        result = fila.apply_action(
            ACTION_APROVAR,
            page_id="page-1",
            current_status=STATUS_AGUARDANDO,
            printer=lambda _m: None,
        )
    mock_client.pages.update.assert_called_once()
    kwargs = mock_client.pages.update.call_args.kwargs
    assert kwargs["page_id"] == "page-1"
    assert kwargs["properties"]["Status"]["select"]["name"] == STATUS_APROVADO
    assert "Canal" not in kwargs["properties"]
    assert result.n8n_fired is False
    assert result.instagram_posted is False
    assert result.published is False
    assert result.written is True


def test_novo_dry_run_forca_nao_publicar():
    mock_client = MagicMock()
    fila = NotionEditorialClient(client=mock_client)
    with patch("editorial.notion_fila.writes_allowed", return_value=False):
        result = fila.apply_action(
            ACTION_NOVO,
            peca="EDI · Post hold",
            braco="Produtora",
            formato="Post",
            printer=lambda _m: None,
        )
    mock_client.pages.create.assert_not_called()
    assert result.dry_run is True
    assert result.transition.properties["Canal"]["select"]["name"] == "Não publicar"


def test_pulse_por_status_e_braco():
    pulse = build_pulse(
        [
            {
                "peca": "A",
                "status": "Aguardando OK",
                "braco": "Editora",
                "numero": "EDI-2",
                "canon_issues": [],
            },
            {
                "peca": "B",
                "status": "Aguardando OK",
                "braco": "Produtora",
                "numero": "EDI-1",
                "canon_issues": [],
            },
            {"peca": "C", "status": "Rascunho", "braco": "Editora", "numero": "EDI-3"},
        ]
    )
    assert pulse["counts"]["Aguardando OK"] == 2
    assert pulse["counts"]["Rascunho"] == 1
    assert pulse["por_braco"]["Editora"] == 2
    assert pulse["por_braco"]["Produtora"] == 1
    assert pulse["proximo"]["peca"] == "B"
    assert pulse["agents"]["Editora"] == "Acervo"
    assert pulse["agents"]["Produtora"] == "Comunicação"


def test_modulo_nao_tem_instagram_api_nem_webhook():
    root = Path(__file__).resolve().parent.parent / "editorial"
    blob = ""
    for path in root.rglob("*.py"):
        blob += path.read_text(encoding="utf-8")
    lowered = blob.lower()
    assert "graph.facebook" not in lowered
    assert "instagram.com/v" not in lowered
    assert "_maybe_post_n8n" not in blob
    assert "N8N_AVANCAR" not in blob
    assert "urllib.request" not in blob
    assert "requests.post" not in blob
    assert "sem webhook" in lowered
    from editorial.status_machine import FORBIDDEN_AGENTS

    assert "AGT-09" in FORBIDDEN_AGENTS
