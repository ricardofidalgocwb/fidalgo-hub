"""Pulso read-only da Fila Editorial: contagens por Status e Braço."""

from __future__ import annotations

from typing import Any

from editorial.status_machine import (
    BRACO_OPTIONS,
    PIPELINE_STATUSES,
    STATUS_AGUARDANDO,
)


def _numero_sort(card: dict[str, Any]) -> tuple:
    raw = card.get("numero") or ""
    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    n = int(digits) if digits else 10**9
    return (n, card.get("peca") or "")


def build_pulse(cards: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {status: 0 for status in PIPELINE_STATUSES}
    by_braco = {braco: 0 for braco in BRACO_OPTIONS}
    by_braco["Sem Braço"] = 0

    waiting: list[dict[str, Any]] = []
    flagged: list[dict[str, Any]] = []
    for card in cards:
        status = card.get("status") or ""
        if status in counts:
            counts[status] += 1
        braco = card.get("braco")
        if braco in by_braco:
            by_braco[braco] += 1
        else:
            by_braco["Sem Braço"] += 1
        if status == STATUS_AGUARDANDO:
            waiting.append(card)
        if card.get("canon_issues"):
            flagged.append(card)

    waiting.sort(key=_numero_sort)
    proximo = waiting[0] if waiting else None
    return {
        "total": len(cards),
        "counts": counts,
        "por_braco": by_braco,
        "proximo": proximo,
        "aguardando": waiting,
        "aprovados": [c for c in cards if c.get("status") == "Aprovado"],
        "rascunhos": [c for c in cards if c.get("status") == "Rascunho"],
        "canon_alertas": flagged,
        "agents": {"Editora": "Acervo", "Produtora": "Comunicação"},
    }
