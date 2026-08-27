"""Carrega IDs canônicos de config/notion_ids.json (sem secrets)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
IDS_PATH = ROOT / "config" / "notion_ids.json"

OS_DATABASE_ID = "e1a7d36b-ae64-821a-b2a2-81970ddf289a"
CRM_OPORTUNIDADES_ID = "6157d36b-ae64-8222-bd17-0188ec6f0c7c"
CLIENTES_ID = "be27d36b-ae64-8313-b646-816b05a657e9"
FINANCEIRO_ID = "5bc7d36b-ae64-8296-80f7-01e5a5ca0ef4"
FILA_FOUNDER_ID = "01cb462a-0237-4aab-9ddc-1735d1e1ea23"
FILA_EDITORIAL_ID = "8af724e1-f396-4864-a1e2-e9840c741047"
FILA_EDITORIAL_DATA_SOURCE_ID = "13be9ea3-a48d-464f-9c10-e15203c3a61a"
MESA_EDITORIAL_PAGE_ID = "3c97d36b-ae64-81ce-b08d-f218c3d02ba8"
ARCHIVED_LEADS_PREFIX = "43b3f514"

FORBIDDEN_EDITORIAL_WRITE_IDS = (
    FILA_FOUNDER_ID,
    OS_DATABASE_ID,
    CRM_OPORTUNIDADES_ID,
    CLIENTES_ID,
    FINANCEIRO_ID,
)


@lru_cache(maxsize=1)
def load_ids() -> dict[str, Any]:
    with IDS_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def fila_founder() -> dict[str, Any]:
    return load_ids()["databases"]["fila_founder"]


def fila_editorial() -> dict[str, Any]:
    return load_ids()["databases"]["fila_editorial"]


def writable_database_ids() -> set[str]:
    """Databases com write=true (hoje: só Fila Founder). Fila Editorial fica de fora."""
    return {
        _compact(db["database_id"])
        for db in load_ids()["databases"].values()
        if db.get("write")
    }


def runner_only_database_ids() -> set[str]:
    """Databases que só o runner dedicado pode tocar (write=false no JSON)."""
    return {
        _compact(db["database_id"])
        for db in load_ids()["databases"].values()
        if db.get("runner_only")
    }


def _compact(value: str) -> str:
    return value.replace("-", "").lower()
