"""Conexão SQLite com foreign_keys ligado em toda sessão."""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from core.errors import EntityIsolationError, GfCoreError, IntegrityFailure, TransitionError

APP_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def default_db_path() -> Path:
    bruto = os.environ.get("GF_CORE_DB")
    if bruto:
        return Path(bruto)
    return APP_ROOT / "data" / "grupo_fidalgo.db"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path) -> None:
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.execute("PRAGMA foreign_keys = ON")
        ativo = int(conn.execute("PRAGMA foreign_keys").fetchone()[0])
        if ativo != 1:
            raise RuntimeError("PRAGMA foreign_keys nao ficou ativo")
        conn.commit()
    finally:
        conn.close()


def traduzir_integrity(exc: sqlite3.IntegrityError) -> GfCoreError:
    texto = str(exc)
    baixo = texto.lower()
    if "foreign key" in baixo:
        return IntegrityFailure("integridade referencial: vinculo inexistente ou registro em uso")
    if "unique" in baixo:
        return IntegrityFailure("cnpj ou numero de serie ja cadastrado")
    if "transicao" in baixo or "faturada" in baixo or "orçamento" in baixo or "orcamento" in baixo:
        return TransitionError(texto)
    if (
        "ef-opex" in baixo
        or "diverge" in baixo
        or "exclusivo" in baixo
        or "incompativel" in baixo
        or "imutavel" in baixo
        or "nao pertence" in baixo
    ):
        return EntityIsolationError(texto)
    return IntegrityFailure(texto)


@contextmanager
def session(db_path: Path):
    conn = connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
