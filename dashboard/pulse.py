"""Pulso read-only da Fila Founder: contagens + próximo item L0."""

from __future__ import annotations

from typing import Any

from dashboard.status_machine import (
    FILA_ORDER,
    PIPELINE_STATUSES,
    STATUS_AGUARDANDO,
    fila_sort_key,
)


def build_pulse(cards: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {status: 0 for status in PIPELINE_STATUSES}
    by_fila = {fila: 0 for fila in FILA_ORDER}
    by_fila["Sem Fila"] = 0

    waiting: list[dict[str, Any]] = []
    for card in cards:
        status = card.get("status") or ""
        if status in counts:
            counts[status] += 1
        fila = card.get("fila")
        if status == STATUS_AGUARDANDO:
            waiting.append(card)
            if fila in by_fila:
                by_fila[fila] += 1
            else:
                by_fila["Sem Fila"] += 1

    waiting.sort(
        key=lambda c: fila_sort_key(c.get("fila"), c.get("nivel_l"), c.get("prioridade"))
    )
    proximo = waiting[0] if waiting else None
    return {
        "total": len(cards),
        "counts": counts,
        "aguardando_por_fila": by_fila,
        "proximo": proximo,
        "fila": waiting,
        "aprovados": [c for c in cards if c.get("status") == "Aprovado"],
        "em_execucao": [c for c in cards if c.get("status") == "Em Execução"],
    }
