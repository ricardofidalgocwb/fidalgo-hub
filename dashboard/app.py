"""Servidor local do Painel Founder (Heros Custom)."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from dashboard.ids import fila_founder, load_ids
from dashboard.notion_fila import (
    NotionFilaClient,
    n8n_avancar_enabled,
    notion_token,
    writes_allowed,
)
from dashboard.pulse import build_pulse
from dashboard.status_machine import PIPELINE_STATUSES, TransitionError

load_dotenv()

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixtures" / "sample_fila.json"

app = Flask(__name__, template_folder=str(ROOT / "templates"))


def _load_cards() -> tuple[list[dict], str]:
    token = notion_token()
    if not token:
        if FIXTURE.exists():
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            return data, "demonstração (sem NOTION_TOKEN)"
        return [], "sem token e sem fixture"
    try:
        cards = NotionFilaClient().query_cards()
        return cards, "live Notion"
    except Exception as exc:  # noqa: BLE001 — painel interno, erro vira aviso
        if FIXTURE.exists():
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            return data, f"fixture (falha live: {exc})"
        raise


def _context() -> dict:
    cards, source = _load_cards()
    pulse = build_pulse(cards)
    cfg = fila_founder()
    token_ok = bool(notion_token())
    return {
        "brand": "Heros Custom",
        "founder": "Ricardo Rodriguez Fidalgo",
        "source": source,
        "token_present": token_ok,
        "writes_ready": writes_allowed(ui_confirmed=True) and token_ok,
        "dry_run_default": not writes_allowed(ui_confirmed=False),
        "n8n_avancar_enabled": n8n_avancar_enabled(),
        "statuses": PIPELINE_STATUSES,
        "pulse": pulse,
        "fila_url": cfg["url"],
        "ids": load_ids(),
    }


@app.get("/")
def index():
    return render_template("index.html", **_context())


@app.get("/api/pulse")
def api_pulse():
    ctx = _context()
    return jsonify(
        {
            "ok": True,
            "source": ctx["source"],
            "token_present": ctx["token_present"],
            "n8n_avancar_enabled": ctx["n8n_avancar_enabled"],
            "pulse": ctx["pulse"],
        }
    )


@app.post("/api/action")
def api_action():
    body = request.get_json(silent=True) or {}
    page_id = (body.get("page_id") or "").strip()
    action = (body.get("action") or "").strip().lower()
    current_status = (body.get("current_status") or "").strip()
    reason = body.get("reason")
    ui_confirmed = bool(body.get("confirmed"))
    if not page_id or not action or not current_status:
        return jsonify({"ok": False, "error": "page_id, action e current_status são obrigatórios"}), 400
    try:
        result = NotionFilaClient().apply_action(
            page_id,
            action,
            current_status,
            reason=reason,
            ui_confirmed=ui_confirmed,
        )
    except TransitionError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"ok": False, "error": str(exc), "dry_run": True}), 200

    return jsonify(
        {
            "ok": True,
            "dry_run": result.dry_run,
            "written": result.written,
            "n8n_fired": result.n8n_fired,
            "message": result.message,
            "payload": result.payload,
            "to_status": result.transition.to_status,
            "fire_n8n": result.transition.fire_n8n,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Painel Founder — Heros Custom")
    parser.add_argument("--host", default=os.getenv("FOUNDER_PANEL_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("FOUNDER_PANEL_PORT", "5050")))
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    print(
        "Painel Founder · Heros Custom · dry-run "
        f"{'ligado' if not writes_allowed(ui_confirmed=False) else 'liberado via CONFIRM=1'}"
    )
    print("Aprovar nunca dispara n8n. Avançar só dispara se N8N_AVANCAR_ENABLED=1.")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
