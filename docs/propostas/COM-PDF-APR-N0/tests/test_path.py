"""Ponte visível no pacote: a guarda pytest continua em tests/ na raiz."""

from pathlib import Path

PACOTE = Path(__file__).resolve().parents[1]
ROOT = PACOTE.parents[2]
GUARD = ROOT / "tests" / "test_com_pdf_apr_n0.py"


def test_guarda_na_raiz_do_repo():
    assert ROOT.name == "fidalgo-hub" or (ROOT / "pytest.ini").is_file()
    assert GUARD.is_file(), f"guarda ausente: {GUARD}"
    assert "COM-PDF-APR-N0" in GUARD.read_text(encoding="utf-8")
