"""HTTP do painel: Aprovar devolve fire_n8n false e dry-run sem token."""

from __future__ import annotations

from dashboard.app import app


def test_pulse_endpoint_sem_token():
    client = app.test_client()
    resp = client.get("/api/pulse")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["n8n_avancar_enabled"] is False
    assert data["pulse"]["proximo"]["fila"] == "1 · L0"


def test_aprovar_api_dry_run_nao_marca_n8n():
    client = app.test_client()
    resp = client.post(
        "/api/action",
        json={
            "page_id": "3c87d36b-ae64-8114-88fa-e83789464782",
            "action": "aprovar",
            "current_status": "Aguardando OK",
            "confirmed": False,
        },
    )
    data = resp.get_json()
    assert data["ok"] is True
    assert data["dry_run"] is True
    assert data["written"] is False
    assert data["n8n_fired"] is False
    assert data["fire_n8n"] is False
    assert data["payload"]["properties"]["Status"]["select"]["name"] == "Aprovado"


def test_avancar_sem_aprovado_falha():
    client = app.test_client()
    resp = client.post(
        "/api/action",
        json={
            "page_id": "page-1",
            "action": "avancar",
            "current_status": "Aguardando OK",
            "confirmed": True,
        },
    )
    assert resp.status_code == 400
    assert "Avançar" in resp.get_json()["error"]


def test_recusar_sem_motivo_falha():
    client = app.test_client()
    resp = client.post(
        "/api/action",
        json={
            "page_id": "page-1",
            "action": "recusar",
            "current_status": "Aguardando OK",
            "reason": "x",
            "confirmed": False,
        },
    )
    assert resp.status_code == 400
    assert "motivo" in resp.get_json()["error"].lower()


def test_home_portugues_heros_custom():
    client = app.test_client()
    html = client.get("/").get_data(as_text=True)
    assert "Heros Custom" in html
    assert "Eros" not in html
    assert "Eletric" not in html
    assert "Aprovar" in html
    assert "Avançar" in html
    assert "Recusar" in html
    assert "Adiar" in html
    assert "Painel Founder" in html
