"""Guarda Cap.2 / Fusca F-P0-1…6 player/páginas unpublished (Heros Custom).

HUB-bancar-executar-1709 · padrão #29 · sem embed real · Hotmart STOP.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "heros-custom"
AULAS = SITE / "aulas"
CAP2 = AULAS / "cap2"
ASSETS = AULAS / "assets"
SRC_CAP2 = ROOT / "docs" / "propostas" / "COM-PDF-CAP2-motor" / "assets"
SRC_N0 = ROOT / "docs" / "propostas" / "COM-PDF-APR-N0" / "assets"

PAGES = [
    CAP2 / "index.html",
    CAP2 / "f-p0-1" / "index.html",
    CAP2 / "f-p0-2" / "index.html",
    CAP2 / "f-p0-3" / "index.html",
    CAP2 / "f-p0-4" / "index.html",
    CAP2 / "f-p0-5" / "index.html",
    CAP2 / "f-p0-6" / "index.html",
]

LESSONS = [
    CAP2 / "f-p0-1" / "index.html",
    CAP2 / "f-p0-2" / "index.html",
    CAP2 / "f-p0-3" / "index.html",
    CAP2 / "f-p0-4" / "index.html",
    CAP2 / "f-p0-5" / "index.html",
    CAP2 / "f-p0-6" / "index.html",
]

TIPADAS_CAP2 = (
    ("Cap2_P0_tinware_AUR1500_SRC-commons.jpg", 483_449),
    ("Cap2_P0_tinware_coccinelle_SRC-commons.jpg", 1_111_977),
    ("Cap2_P0_prefixBD_crop_SRC-commons.jpg", 241_948),
    ("Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg", 708_229),
    ("Cap2_P0_tinware_1965AVI_SRC-commons.jpg", 409_825),
)

TIPADAS_N0 = (
    ("N0_caixa8_fuseBox8polos_SRC-appletree.jpg", 129_434),
    ("N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg", 239_795),
    ("N0_A8_dinam_SRC-heritagestocks.jpg", 443_360),
    ("N0_A8_alt_SRC-appletreekit.jpg", 141_153),
)

HEADINGS = ("O quê", "Por quê", "Como", "Cheque", "Erro comum", "Próximo")

BANNED = re.compile(
    r"""
    (?:R\$)
    | (?:preço)
    | (?:\bpreco\b)
    | (?:hotmart)
    | (?:whatsapp)
    | (?:\bwa\.me\b)
    | (?:\bzap\b)
    | (?:\bnap\b)
    | (?:os\s+viva)
    | (?:olímio)
    | (?:olimio)
    | (?:99187)
    | (?:youtube)
    | (?:vimeo)
    | (?:youtu\.be)
    """,
    re.I | re.X,
)

DRIVE_ID_RE = re.compile(r"\b1[A-Za-z0-9_-]{20,}\b")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _all_html() -> str:
    return "\n".join(_read(p) for p in PAGES)


def test_indice_e_seis_paginas_existem():
    for page in PAGES:
        assert page.is_file(), page
    index = _read(CAP2 / "index.html")
    for slug in (
        "f-p0-1/",
        "f-p0-2/",
        "f-p0-3/",
        "f-p0-4/",
        "f-p0-5/",
        "f-p0-6/",
    ):
        assert slug in index
    aulas_index = _read(AULAS / "index.html")
    assert "cap2/" in aulas_index
    assert "F-P0-1" in aulas_index
    assert (CAP2 / "README.md").is_file()


def test_arco_em_cada_aula():
    for page in LESSONS:
        html = _read(page)
        for heading in HEADINGS:
            assert f"<h2>{heading}</h2>" in html, (page.parent.name, heading)
        assert "F-P0-" in html


def test_ids_oficiais_nao_sozinhos():
    blob = _all_html()
    assert "F-P0-1" in blob
    assert "F-P0-6" in blob
    assert re.search(r"(?<!F-P0-)\bF[1-6]\b", blob) is None


def test_sem_padroes_comerciais():
    blob = _all_html()
    match = BANNED.search(blob)
    assert match is None, match.group(0) if match else None
    captions = "\n".join(
        re.findall(r"<figcaption>(.*?)</figcaption>", blob, flags=re.S)
    )
    assert DRIVE_ID_RE.search(captions) is None
    assert "staff" not in blob.lower()
    assert "g-pass" not in blob.lower()


def test_sem_iframe_youtube_vimeo():
    blob = _all_html().lower()
    assert "<iframe" not in blob
    assert "youtube" not in blob
    assert "vimeo" not in blob
    assert ".mp4" not in blob


def test_banner_unpublished_e_noindex():
    for page in PAGES:
        html = _read(page)
        assert 'lang="pt-BR"' in html
        assert "noindex" in html
        assert "UNPUBLISHED · DRAFT · Founder OK required to go live" in html
        assert "vídeo em elaboração · unpublished" in html
    css = _read(SITE / "css" / "site.css")
    assert "#C9A227" in css or "#c9a227" in css
    assert "Montserrat" in css
    assert "Inter" in css
    assert ".track-nav" in css


def test_fp0_3_tipadas_filenames_e_bytes_exactos():
    html = _read(CAP2 / "f-p0-3" / "index.html")
    assert "Cap2_P0_tinware_AUR1500_SRC-commons.jpg" in html
    assert "Cap2_P0_tinware_coccinelle_SRC-commons.jpg" in html
    assert "Cap2_P0_prefixBD_crop_SRC-commons.jpg" in html
    assert "Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg" in html
    assert "Cap2_P0_tinware_1965AVI_SRC-commons.jpg" in html
    assert "latas no lugar (motor 1500)" in html
    assert "latas no lugar (Coccinelle)" in html
    assert "prefixo no bloco" in html
    assert "ventoinha e correia" in html
    for name, expected in TIPADAS_CAP2:
        path = ASSETS / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size == expected, (name, size, expected)
        assert size >= 100_000, (name, size)
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", name
        source = SRC_CAP2 / name
        assert source.is_file(), name
        assert path.read_bytes() == source.read_bytes(), name


def test_fp0_5_reusa_tipadas_n0_bytes_exactos():
    html = _read(CAP2 / "f-p0-5" / "index.html")
    assert "N0_caixa8_fuseBox8polos_SRC-appletree.jpg" in html
    assert "N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg" in html
    assert "N0_A8_dinam_SRC-heritagestocks.jpg" in html
    assert "N0_A8_alt_SRC-appletreekit.jpg" in html
    assert "8 pólos" in html
    assert "12 pólos" in html
    assert "isto é dínamo" in html
    assert "isto é alternador" in html
    for name, expected in TIPADAS_N0:
        path = ASSETS / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size == expected, (name, size, expected)
        source = SRC_N0 / name
        if source.is_file():
            assert path.read_bytes() == source.read_bytes(), name


def test_subnav_n0_e_cap2():
    aulas_index = _read(AULAS / "index.html")
    cap2_index = _read(CAP2 / "index.html")
    assert "Cap.2 / Passaporte P0" in aulas_index
    assert "Cap.2 / Passaporte P0" in cap2_index
    aulas_nav = aulas_index.split('aria-label="Trilhas de aulas"', 1)[1].split(
        "</nav>", 1
    )[0]
    assert "N0" in aulas_nav
    assert 'aria-current="page"' in aulas_nav
    header = aulas_index.split('aria-label="Principal"', 1)[1].split("</nav>", 1)[0]
    assert "Aulas" in header


def test_readme_cita_notion_roteiros():
    readme = _read(CAP2 / "README.md")
    assert "3de7d36bae64811286aad405b7ad3059" in readme
    assert "3de7d36bae6481938a1bf1bbbb31a0d4" in readme
    miolo = _all_html()
    assert "3de7d36bae64811286aad405b7ad3059" not in miolo
    assert "3de7d36bae6481938a1bf1bbbb31a0d4" not in miolo
    assert "notion.com" not in miolo.lower()
