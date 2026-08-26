"""Aprovar não pode acionar n8n; escritas Notion ficam atrás do token."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from dashboard.notion_fila import NotionFilaClient, writes_allowed
from dashboard.status_machine import (
    ACTION_APROVAR,
    ACTION_AVANCAR,
    STATUS_AGUARDANDO,
    STATUS_APROVADO,
)


def test_writes_allowed_sem_token():
    with patch.dict("os.environ", {"NOTION_TOKEN": "", "CONFIRM": "1"}, clear=False):
        with patch("dashboard.notion_fila.notion_token", return_value=None):
            assert writes_allowed(ui_confirmed=True) is False
            assert writes_allowed(ui_confirmed=False) is False


def test_writes_allowed_token_e_confirm():
    with patch("dashboard.notion_fila.notion_token", return_value="ntn_test"):
        with patch("dashboard.notion_fila.confirm_env", return_value=True):
            assert writes_allowed(ui_confirmed=False) is True


def test_writes_allowed_token_e_ui_confirmada():
    with patch("dashboard.notion_fila.notion_token", return_value="ntn_test"):
        with patch("dashboard.notion_fila.confirm_env", return_value=False):
            assert writes_allowed(ui_confirmed=True) is True
            assert writes_allowed(ui_confirmed=False) is False


def test_aprovar_dry_run_nao_chama_pages_update():
    mock_client = MagicMock()
    fila = NotionFilaClient(client=mock_client)
    with patch("dashboard.notion_fila.notion_token", return_value="ntn_test"):
        with patch("dashboard.notion_fila.writes_allowed", return_value=False):
            result = fila.apply_action(
                "page-1",
                ACTION_APROVAR,
                STATUS_AGUARDANDO,
                ui_confirmed=False,
                printer=lambda _m: None,
            )
    mock_client.pages.update.assert_not_called()
    assert result.dry_run is True
    assert result.written is False
    assert result.n8n_fired is False
    assert result.transition.fire_n8n is False


def test_aprovar_live_nao_posta_n8n():
    mock_client = MagicMock()
    fila = NotionFilaClient(client=mock_client)
    with patch("dashboard.notion_fila.notion_token", return_value="ntn_test"):
        with patch("dashboard.notion_fila.writes_allowed", return_value=True):
            with patch("dashboard.notion_fila.n8n_avancar_enabled", return_value=True):
                with patch("dashboard.notion_fila._maybe_post_n8n") as post:
                    result = fila.apply_action(
                        "page-1",
                        ACTION_APROVAR,
                        STATUS_AGUARDANDO,
                        ui_confirmed=True,
                        printer=lambda _m: None,
                    )
    mock_client.pages.update.assert_called_once()
    kwargs = mock_client.pages.update.call_args.kwargs
    assert kwargs["page_id"] == "page-1"
    assert kwargs["properties"]["Status"]["select"]["name"] == STATUS_APROVADO
    post.assert_not_called()
    assert result.n8n_fired is False
    assert result.written is True


def test_avancar_so_chama_n8n_quando_habilitado():
    mock_client = MagicMock()
    fila = NotionFilaClient(client=mock_client)
    with patch("dashboard.notion_fila.notion_token", return_value="ntn_test"):
        with patch("dashboard.notion_fila.writes_allowed", return_value=True):
            with patch("dashboard.notion_fila.n8n_avancar_enabled", return_value=True):
                with patch("dashboard.notion_fila._maybe_post_n8n", return_value=True) as post:
                    result = fila.apply_action(
                        "page-2",
                        ACTION_AVANCAR,
                        STATUS_APROVADO,
                        ui_confirmed=True,
                        printer=lambda _m: None,
                    )
    post.assert_called_once()
    assert result.n8n_fired is True


def test_avancar_padrao_nao_chama_n8n():
    mock_client = MagicMock()
    fila = NotionFilaClient(client=mock_client)
    with patch("dashboard.notion_fila.notion_token", return_value="ntn_test"):
        with patch("dashboard.notion_fila.writes_allowed", return_value=True):
            with patch("dashboard.notion_fila.n8n_avancar_enabled", return_value=False):
                with patch("dashboard.notion_fila._maybe_post_n8n") as post:
                    result = fila.apply_action(
                        "page-2",
                        ACTION_AVANCAR,
                        STATUS_APROVADO,
                        ui_confirmed=True,
                        printer=lambda _m: None,
                    )
    post.assert_not_called()
    assert result.n8n_fired is False
    assert result.written is True


def test_pulse_l0_primeiro():
    from dashboard.pulse import build_pulse

    pulse = build_pulse(
        [
            {
                "name": "Caixa",
                "status": "Aguardando OK",
                "fila": "3 · Caixa",
                "nivel_l": "L4 Caixa/Margem",
                "prioridade": "Alta",
            },
            {
                "name": "Hold L0",
                "status": "Aguardando OK",
                "fila": "1 · L0",
                "nivel_l": "L0 Segurança",
                "prioridade": "Crítica",
            },
            {"name": "Feito", "status": "Concluído", "fila": "4 · Demais"},
        ]
    )
    assert pulse["counts"]["Aguardando OK"] == 2
    assert pulse["counts"]["Concluído"] == 1
    assert pulse["proximo"]["name"] == "Hold L0"
    assert pulse["aguardando_por_fila"]["1 · L0"] == 1
