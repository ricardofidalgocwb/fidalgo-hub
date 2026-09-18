"""Guarda N0 A1–A6 player/páginas unpublished (Heros Custom).

HUB-videoaula-roteiros-p0-1309 · sem embed real · Hotmart STOP.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "heros-custom"
AULAS = SITE / "aulas"
ASSETS = AULAS / "assets"
SRC_N0 = ROOT / "docs" / "propostas" / "COM-PDF-APR-N0" / "assets"

PAGES = [
    AULAS / "index.html",
    AULAS / "a1" / "index.html",
    AULAS / "a2" / "index.html",
    AULAS / "a3" / "index.html",
    AULAS / "a4" / "index.html",
    AULAS / "a5" / "index.html",
    AULAS / "a6" / "index.html",
]

LESSONS = [
    AULAS / "a1" / "index.html",
    AULAS / "a2" / "index.html",
    AULAS / "a3" / "index.html",
    AULAS / "a4" / "index.html",
    AULAS / "a5" / "index.html",
    AULAS / "a6" / "index.html",
]

TIPADAS = (
    ("N0_A8_dinam_SRC-heritagestocks.jpg", 443_360),
    ("N0_A8_alt_SRC-appletreekit.jpg", 141_153),
    ("N0_caixa8_fuseBox8polos_SRC-appletree.jpg", 129_434),
    ("N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg", 239_795),
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
    index = _read(AULAS / "index.html")
    for slug in ("a1/", "a2/", "a3/", "a4/", "a5/", "a6/"):
        assert slug in index
    assert (AULAS / "README.md").is_file()


def test_arco_em_cada_aula():
    for page in LESSONS:
        html = _read(page)
        for heading in HEADINGS:
            assert f"<h2>{heading}</h2>" in html, (page.name, heading)


def test_sem_padroes_comerciais():
    blob = _all_html()
    match = BANNED.search(blob)
    assert match is None, match.group(0) if match else None
    captions = "\n".join(
        re.findall(r"<figcaption>(.*?)</figcaption>", blob, flags=re.S)
    )
    assert DRIVE_ID_RE.search(captions) is None
    assert "staff" not in blob.lower()


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


def test_a3_a4_tipadas_filenames_e_bytes_exactos():
    a3 = _read(AULAS / "a3" / "index.html")
    a4 = _read(AULAS / "a4" / "index.html")
    assert "N0_A8_dinam_SRC-heritagestocks.jpg" in a3
    assert "N0_A8_alt_SRC-appletreekit.jpg" in a3
    assert "isto é dínamo" in a3
    assert "isto é alternador" in a3
    assert "N0_caixa8_fuseBox8polos_SRC-appletree.jpg" in a4
    assert "N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg" in a4
    assert "8 pólos" in a4
    assert "12 pólos" in a4
    for name, expected in TIPADAS:
        path = ASSETS / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size == expected, (name, size, expected)
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", name
        source = SRC_N0 / name
        if source.is_file():
            assert path.read_bytes() == source.read_bytes(), name


def test_nav_aulas_no_mvp_e_siblings():
    siblings = [
        SITE / "index.html",
        SITE / "servicos" / "index.html",
        SITE / "prova" / "index.html",
        SITE / "como" / "index.html",
        SITE / "pecas" / "index.html",
        SITE / "contato" / "index.html",
    ]
    for page in siblings:
        html = _read(page)
        nav = html.split('aria-label="Principal"', 1)[1].split("</nav>", 1)[0]
        assert "Aulas" in nav, page


def test_narrador_oliver_persona():
    for page in PAGES:
        html = _read(page)
        assert "Narrador: Oliver" in html, page
    assert "<iframe" not in _all_html().lower()


def test_readme_cita_notion_roteiros():
    readme = _read(AULAS / "README.md")
    assert "3da7d36bae6481d098e2f5e59e89e1d0" in readme
    assert "HUB-videoaula-roteiros-p0-1309" in readme
    miolo = _all_html()
    assert "3da7d36bae6481d098e2f5e59e89e1d0" not in miolo
    assert "notion.com" not in miolo.lower()
