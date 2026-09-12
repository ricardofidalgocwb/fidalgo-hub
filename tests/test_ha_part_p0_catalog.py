"""Guarda HA-PART P0 catalog slots unpublished (Heros Custom).

HUB-hapart-catalogo-p0-1209 · ACE Mestra · T1 · sem Loja no HTML.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "heros-custom"
ASSETS = SITE / "pecas" / "assets"
HTML = SITE / "pecas" / "index.html"

TIPADAS = (
    ("HA-PART-MO-0001_SRC-appletree_boschBlue.jpg", 173_880, "bobina", False),
    ("HA-PART-MO-0002_SRC-appletree_pertronix.jpg", 123_862, "distrib", True),
    ("HA-PART-MO-0003_SRC-appletree_cap03010.jpg", 131_675, "tampa", False),
    ("HA-PART-MO-0005_SRC-appletree_boschWires.jpg", 138_024, "cabos", False),
    ("HA-PART-MO-0006_SRC-appletree_WR8AC.jpg", 121_958, "WR8AC", False),
    ("HA-PART-MO-0009_SRC-appletree_regulator.jpg", 191_099, "regulador", False),
    ("HA-PART-MO-0012_SRC-heritage_starter.jpg", 387_782, "arranque", False),
    ("HA-PART-CAB_chave_SRC-heritage.jpg", 319_786, "chave", False),
    ("HA-PART-MO-0031_SRC-heritage_Bplus.jpg", 105_117, "B+", True),
    ("HA-PART-MO-0032_SRC-appletree_groundStrap.jpg", 168_519, "malha", False),
)

PRICE_RE = re.compile(
    r"""
    (?:R\$)
    | (?:preço)
    | (?:\bpreco\b)
    | (?:\bprice\b)
    | (?:checkout)
    | (?:carrinho)
    | (?:hotmart)
    """,
    re.I | re.X,
)


def test_dez_assets_existem_com_bytes_exactos():
    for name, expected, _label, _soft in TIPADAS:
        path = ASSETS / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size == expected, (name, size, expected)
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", name


def test_html_lista_filenames_e_labels():
    html = HTML.read_text(encoding="utf-8")
    for name, _expected, label, _soft in TIPADAS:
        assert name in html, name
        assert label in html, label
        part_id = name.split("_SRC-")[0]
        assert part_id in html, part_id


def test_html_sem_padroes_de_loja():
    html = HTML.read_text(encoding="utf-8")
    match = PRICE_RE.search(html)
    assert match is None, match.group(0) if match else None


def test_soft_0002_e_0031_visiveis():
    html = HTML.read_text(encoding="utf-8")
    assert "HA-PART-MO-0002" in html
    assert "HA-PART-MO-0031" in html
    assert "soft · aftermarket cite" in html
    block_0002 = html[html.find("HA-PART-MO-0002_SRC-appletree_pertronix") - 400 :][:900]
    block_0031 = html[html.find("HA-PART-MO-0031_SRC-heritage_Bplus") - 400 :][:900]
    assert "soft" in block_0002.lower()
    assert "soft" in block_0031.lower()


def test_robots_noindex():
    html = HTML.read_text(encoding="utf-8")
    assert 'name="robots"' in html
    assert "noindex" in html
    assert "nofollow" in html
    assert "UNPUBLISHED · DRAFT" in html
