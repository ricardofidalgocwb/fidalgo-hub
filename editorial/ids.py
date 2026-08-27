"""IDs da Fila Editorial a partir do SSOT único `config/notion_ids.json`."""

from __future__ import annotations

from typing import Any

from dashboard.ids import (
    FILA_EDITORIAL_DATA_SOURCE_ID,
    FILA_EDITORIAL_ID,
    MESA_EDITORIAL_ID,
    fila_editorial,
    load_ids,
)

__all__ = [
    "FILA_EDITORIAL_DATA_SOURCE_ID",
    "FILA_EDITORIAL_ID",
    "MESA_EDITORIAL_ID",
    "fila_editorial",
    "load_ids",
]


def compact_id(value: str) -> str:
    return (value or "").replace("-", "").lower()


def assert_editorial_database(database_id: str) -> None:
    from editorial.status_machine import TransitionError

    if compact_id(database_id) != compact_id(FILA_EDITORIAL_ID):
        raise TransitionError(
            "Runner editorial só escreve na Fila Editorial "
            f"({FILA_EDITORIAL_ID})."
        )


def agent_for_braco(braco: str | None) -> str | None:
    cfg: dict[str, Any] = fila_editorial()
    agents = cfg.get("agents") or {}
    if not braco:
        return None
    return agents.get(braco)
