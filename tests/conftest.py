"""Ambiente seguro para testes: sem CONFIRM e sem webhook n8n."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolate_write_env(monkeypatch):
    monkeypatch.setenv("CONFIRM", "0")
    monkeypatch.delenv("N8N_AVANCAR_ENABLED", raising=False)
    monkeypatch.delenv("N8N_AVANCAR_WEBHOOK", raising=False)
    monkeypatch.delenv("N8N_WEBHOOK_KEY", raising=False)
    monkeypatch.delenv("HEROS_WEBHOOK_KEY", raising=False)
