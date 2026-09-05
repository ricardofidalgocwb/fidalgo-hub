"""Guarda COM-VIS-H1-M6: três tipadas Commons ≥100 KB; DUPs e N0-H1 fora."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs" / "acervo" / "vis-tipadas"
README = PACK / "README.md"
SOURCES = PACK / "SOURCES.md"
N0_HTML = ROOT / "docs" / "propostas" / "COM-PDF-APR-N0" / "index.html"

MIN_BYTES = 100_000

TIPADAS = (
    ("H1_VW_Beetle_1946_SRC-commons.jpg", 512_333),
    ("H1_KdF_Wagen42_SRC-commons.jpg", 434_867),
    ("M6_T_motor30PS1959_SRC-commons.jpg", 578_324),
)

BANNED_NAMES = (
    "Cap2_engineBay",
    "M6_T_engineBayTin",
    "Cap2_engine1962",
    "N0_A8_engineGenAlt",
    "N0_A8_1953_1200",
    "HenryFord",
    "Henry_Ford",
)


def test_tres_tipadas_existem_e_ge_100kb():
    for name, expected in TIPADAS:
        path = PACK / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size >= MIN_BYTES, (name, size)
        assert size == expected, (name, size, expected)
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", name


def test_readme_sources_citam_commons_drive_e_indice_vis():
    readme = README.read_text(encoding="utf-8")
    sources = SOURCES.read_text(encoding="utf-8")
    blob = f"{readme}\n{sources}".lower()
    assert "não publicado" in blob or "nao publicado" in blob
    assert "vis-g1" in blob
    assert "m6" in blob
    assert "1vjvvz18dygureyefyfzvadloa3ohgwbp" in blob
    assert "1kd6y75j_hczhb4cug9r9mhoftcf4aent" in blob
    assert "1baczvk65rsvs5xhe-fhin9ileq-hovjw" in blob
    assert "commons.wikimedia.org" in blob
    assert "3d27d36bae6481e8a8d8ed280f9acbdd" in blob
    assert "n0-h1" in blob
    assert "1959–66" in f"{readme}\n{sources}" or "1959-66" in blob


def test_dups_e_fail_candidates_fora_do_pacote():
    names = [p.name for p in PACK.iterdir() if p.is_file()]
    joined = " ".join(names)
    for banned in BANNED_NAMES:
        assert banned not in joined, banned
    assert not any("engineBayTin" in n for n in names)
    assert not any(n.startswith("N0_A8_") for n in names)


def test_nao_sobrescreve_n0_h1_era_b1():
    html = N0_HTML.read_text(encoding="utf-8")
    assert "H1 · Era B1 (1959–66)" in html
    assert "N0-H1" in html
    assert "<img" not in html.lower()
    assert "H1_VW_Beetle_1946" not in html
    assert "H1_KdF_Wagen42" not in html
    assert "KdF-Wagen" not in html
