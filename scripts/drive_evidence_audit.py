#!/usr/bin/env python3
"""Audit offline de evidência Drive — portão stub vs solid.

Dry-only: não chama a API Drive, não escreve Notion, não liga n8n.
Aceita um manifesto JSON {name, size, id} (lista ou {"files": [...]}).

Classificação (mesmo limiar do upload resumable):
  size ≤ 100 000  → stub
  size > 100 000  → solid

Compara nomes com o catálogo de tipagem em config/drive_ids.json.
Exit ≠ 0 se houver stub ou size inválido. Lacuna de tipagem só é reportada.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from scripts.drive_resumable_upload import MIN_EVIDENCE_BYTES

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DRIVE_IDS = REPO_ROOT / "config" / "drive_ids.json"

# mimeType Drive de pasta — sem campo size útil.
_FOLDER_MIME = "application/vnd.google-apps.folder"


class DriveAuditError(Exception):
    """Manifesto inválido ou portão falhou (stubs)."""


def load_drive_ids(path: Path | None = None) -> dict[str, Any]:
    """Lê config/drive_ids.json (ou outro path). Sem rede."""
    target = path or DEFAULT_DRIVE_IDS
    if not target.is_file():
        raise DriveAuditError(f"drive_ids não encontrado: {target}")
    with target.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise DriveAuditError("drive_ids.json tem de ser um objeto JSON.")
    return data


def tipagem_catalog(drive_ids: dict[str, Any] | None = None) -> list[str]:
    ids = drive_ids if drive_ids is not None else load_drive_ids()
    slots = ids.get("tipagem_slots") or []
    if not isinstance(slots, list):
        raise DriveAuditError("tipagem_slots tem de ser uma lista.")
    return [str(s) for s in slots]


def _as_int_size(raw: Any) -> int | None:
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def classify_size(size: int, min_bytes: int = MIN_EVIDENCE_BYTES) -> str:
    """≤ min_bytes → stub; > min_bytes → solid."""
    if size <= min_bytes:
        return "stub"
    return "solid"


def classify_item(
    item: dict[str, Any],
    min_bytes: int = MIN_EVIDENCE_BYTES,
) -> dict[str, Any]:
    """Classifica um item do manifesto. Pastas são ignoradas (kind=folder)."""
    name = str(item.get("name") or "")
    file_id = item.get("id")
    mime = str(item.get("mimeType") or item.get("mime_type") or "")
    if mime == _FOLDER_MIME or item.get("kind") == "folder":
        return {
            "name": name,
            "id": file_id,
            "kind": "folder",
            "class": "skip",
            "size": _as_int_size(item.get("size")),
        }
    size = _as_int_size(item.get("size"))
    if size is None:
        return {
            "name": name,
            "id": file_id,
            "kind": "file",
            "class": "invalid",
            "size": None,
            "error": "size em falta ou inválido",
        }
    return {
        "name": name,
        "id": file_id,
        "kind": "file",
        "class": classify_size(size, min_bytes=min_bytes),
        "size": size,
    }


def slot_tokens(slot: str) -> list[str]:
    """Tokens de match a partir do id do slot (02_farol_E, 03_chicote/lanterna)."""
    raw = slot.strip().lower()
    tokens: list[str] = [raw]
    for alt in raw.split("/"):
        alt = alt.strip()
        if not alt:
            continue
        tokens.append(alt)
        stripped = re.sub(r"^\d+_", "", alt)
        if stripped and stripped != alt:
            tokens.append(stripped)
    # únicos, mais longos primeiro — evita match vazio
    seen: set[str] = set()
    ordered: list[str] = []
    for tok in sorted(tokens, key=len, reverse=True):
        if tok and tok not in seen:
            seen.add(tok)
            ordered.append(tok)
    return ordered


def filename_matches_slot(name: str, slot: str) -> bool:
    hay = name.lower()
    return any(tok in hay for tok in slot_tokens(slot))


def tipagem_coverage(
    names: list[str],
    catalog: list[str],
) -> dict[str, Any]:
    present: list[str] = []
    gaps: list[str] = []
    hits: dict[str, list[str]] = {}
    for slot in catalog:
        matched = [n for n in names if filename_matches_slot(n, slot)]
        if matched:
            present.append(slot)
            hits[slot] = matched
        else:
            gaps.append(slot)
    return {"present": present, "gaps": gaps, "hits": hits}


def parse_manifest(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        files = raw.get("files")
        if files is None:
            raise DriveAuditError(
                "Manifesto objeto precisa da chave 'files' (lista de {name,size,id})."
            )
        raw = files
    if not isinstance(raw, list):
        raise DriveAuditError("Manifesto tem de ser uma lista ou {\"files\": [...]}.")
    items: list[dict[str, Any]] = []
    for idx, row in enumerate(raw):
        if not isinstance(row, dict):
            raise DriveAuditError(f"Item {idx} do manifesto não é um objeto.")
        items.append(row)
    return items


def load_manifest(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise DriveAuditError(f"Manifesto não encontrado: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DriveAuditError(f"Manifesto JSON inválido: {exc}") from exc
    return parse_manifest(data)


def audit_manifest(
    items: list[dict[str, Any]],
    *,
    drive_ids: dict[str, Any] | None = None,
    min_bytes: int | None = None,
) -> dict[str, Any]:
    """Audita o manifesto. Não chama Drive."""
    ids = drive_ids if drive_ids is not None else load_drive_ids()
    threshold = (
        min_bytes
        if min_bytes is not None
        else int(ids.get("min_evidence_bytes") or MIN_EVIDENCE_BYTES)
    )
    catalog = tipagem_catalog(ids)
    classified = [classify_item(it, min_bytes=threshold) for it in items]
    files = [c for c in classified if c["kind"] == "file"]
    stubs = [c for c in files if c["class"] == "stub"]
    solids = [c for c in files if c["class"] == "solid"]
    invalids = [c for c in files if c["class"] == "invalid"]
    coverage = tipagem_coverage(
        [c["name"] for c in solids],
        catalog,
    )
    failed = bool(stubs or invalids)
    return {
        "dry_run": True,
        "written": False,
        "n8n": False,
        "live_drive": False,
        "min_bytes": threshold,
        "ok": not failed,
        "counts": {
            "files": len(files),
            "solid": len(solids),
            "stub": len(stubs),
            "invalid": len(invalids),
            "folders_skipped": sum(1 for c in classified if c["kind"] == "folder"),
        },
        "stubs": stubs,
        "solids": solids,
        "invalid": invalids,
        "tipagem": {
            "catalog": catalog,
            "present": coverage["present"],
            "gaps": coverage["gaps"],
            "hits": coverage["hits"],
        },
        "os34": ids.get("os34"),
        "message": (
            f"{len(solids)} solid / {len(stubs)} stub / {len(invalids)} inválido; "
            f"tipagem gaps: {coverage['gaps'] or 'nenhuma'}."
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit dry-only de evidência Drive (stub ≤100 KB vs solid). "
            "Exige --manifest. Sem API live, sem Notion, sem n8n."
        )
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="JSON de {name,size,id} (lista ou {\"files\": [...]})",
    )
    parser.add_argument(
        "--drive-ids",
        default=str(DEFAULT_DRIVE_IDS),
        help="Path do catálogo drive_ids.json",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        items = load_manifest(Path(args.manifest).expanduser())
        drive_ids = load_drive_ids(Path(args.drive_ids).expanduser())
        report = audit_manifest(items, drive_ids=drive_ids)
    except DriveAuditError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("ok") else 2


if __name__ == "__main__":
    sys.exit(main())
