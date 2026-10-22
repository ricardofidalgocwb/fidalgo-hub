"""Backup local do sqlite: zip deflacionado com nome RNA Atlas."""

from __future__ import annotations

import sqlite3
import zipfile
from datetime import date
from pathlib import Path

from core.entities import validar_entidade
from core.rna_atlas import gerar_caminho


def criar_backup(
    db_path: Path,
    dest_dir: Path,
    *,
    tag: str,
    quando: date | None = None,
) -> Path:
    validar_entidade(tag)
    dest_dir.mkdir(parents=True, exist_ok=True)
    snapshot = dest_dir / ".snapshot.db"
    try:
        origem = sqlite3.connect(db_path)
        destino = sqlite3.connect(snapshot)
        try:
            origem.backup(destino)
        finally:
            destino.close()
            origem.close()
        existentes = [item.name for item in dest_dir.iterdir()]
        nome = gerar_caminho(tag, "Backup SQLite", "zip", quando=quando, existentes=existentes)
        alvo = dest_dir / nome
        with zipfile.ZipFile(alvo, "w", compression=zipfile.ZIP_DEFLATED) as pacote:
            pacote.write(snapshot, arcname="grupo_fidalgo.db")
        return alvo
    finally:
        snapshot.unlink(missing_ok=True)
