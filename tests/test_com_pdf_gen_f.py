"""Guarda COM-PDF-GEN-F-fusca: 1º e-book gênese unpublished, Gold v1.1.

HUB-ebook-fusca-genesis-1709 · TEC cânon · ACE inventário · Hotmart STOP.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACOTE = ROOT / "docs" / "propostas" / "COM-PDF-GEN-F-fusca"
HTML = PACOTE / "index.html"
README = PACOTE / "README.md"
CSS = PACOTE / "print.css"
PDF = PACOTE / "COM-PDF-GEN-F-fusca.pdf"
ASSETS = PACOTE / "assets"

TIPADAS = (
    ("H1_VW_Beetle_1946_SRC-commons.jpg", 519_609),
    ("H1_KdF_Wagen42_SRC-commons.jpg", 434_867),
    ("Cap2_P0_tinware_AUR1500_SRC-commons.jpg", 483_449),
    ("Cap2_P0_tinware_coccinelle_SRC-commons.jpg", 1_111_977),
    ("N0_caixa8_fuseBox8polos_SRC-appletree.jpg", 129_434),
    ("N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg", 239_795),
    ("N0_A8_dinam_SRC-heritagestocks.jpg", 443_360),
    ("N0_A8_alt_SRC-appletreekit.jpg", 141_153),
)

CAPS = (
    "GEN-F1 — Origem Type 1 / KdF",
    "GEN-F2 — Por quê aircooled",
    "GEN-F3 — Mobilidade família",
    "GEN-F4 — Indústria mundo + BR",
    "GEN-F5 — Ponte Passaporte",
)

ARCO = ("O quê", "Por quê", "Como", "Cheque", "Erro", "Próximo")


def _html() -> str:
    return HTML.read_text(encoding="utf-8")


def _read(*paths: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in paths)


def _figcaptions(html: str) -> list[str]:
    return re.findall(r"<figcaption\b[^>]*>(.*?)</figcaption>", html, flags=re.S | re.I)


def test_artefatos_existem():
    assert HTML.is_file()
    assert README.is_file()
    assert CSS.is_file()
    assert (PACOTE / "emitir-pdf.sh").is_file()
    assert PDF.is_file()
    assert PDF.stat().st_size > 10_000


def test_cinco_capitulos_gen_f():
    html = _html()
    for cap in CAPS:
        assert cap in html, cap
    for aula_id in ("gen-f1", "gen-f2", "gen-f3", "gen-f4", "gen-f5"):
        assert f'id="{aula_id}"' in html, aula_id
    assert "GEN-F1…GEN-F5" in html or "GEN-F1…F5" in html


def test_nao_publicado_e_pt_br():
    html = _html()
    assert 'lang="pt-BR"' in html
    assert "noindex" in html
    assert "UNPUBLISHED" in html
    assert "NÃO PUBLICADO" in html or "Não publicar" in html
    assert "sem site até OK Founder" in html or "sem site até ok founder" in html.lower()
    readme = README.read_text(encoding="utf-8")
    assert "não publicado" in readme.lower() or "nao publicado" in readme.lower()
    assert "separado" in readme.lower()


def test_canon_1968_1996_e_gates():
    html = _html()
    assert "1968" in html
    assert "1996" in html
    assert "12 V ≠ alternador" in html or "12 V ≠ alt" in html
    assert "Type 1 ≠ Type 3" in html
    assert "1993–96" in html or "1993-96" in html
    assert "Itamar" in html
    assert "México" in html or "Mexico" in html.lower()
    assert "2003" in html
    assert "fora" in html.lower()
    assert "03/01/1959" in html
    assert "18/11/1959" in html
    html_l = html.lower()
    assert "47.700" not in html
    assert "47700" not in html
    assert not re.search(r"\b\d+\s*cv\b", html_l)
    assert "torque" not in html_l
    assert "kgfm" not in html_l
    assert "Type 3 = outro módulo" in html or "Type 3 é outro módulo" in html


def test_arco_instrutivo_por_capitulo():
    html = _html()
    for aula_id in ("gen-f1", "gen-f2", "gen-f3", "gen-f4", "gen-f5"):
        bloco = re.search(
            rf'<section[^>]*id="{aula_id}"[^>]*>(.*?)</section>',
            html,
            flags=re.S,
        )
        assert bloco, aula_id
        body = bloco.group(1)
        for label in ARCO:
            assert label in body, (aula_id, label)
        assert "Nesta aula você vai" in body
        assert "você" in body.lower()
    assert html.count("Nesta aula você vai") >= 5
    assert html.count('class="write"') >= 5


def test_zero_rs_hotmart_e_cortes():
    blob = _read(HTML, CSS, README)
    html_css = _read(HTML, CSS)
    lower = blob.lower()
    html_css_lower = html_css.lower()
    assert "R$" not in blob
    assert "hotmart" not in html_css_lower
    assert "whatsapp" not in html_css_lower
    assert "nap" not in html_css_lower
    assert not re.search(r"\bzap\b", html_css_lower)
    assert "staff" not in html_css_lower
    assert "os viva" not in html_css_lower
    assert "path a" not in html_css_lower
    assert "Theodoro" not in blob
    assert "Diogo" not in blob
    assert not re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", blob)
    assert "notion.so" not in html_css_lower
    assert "instagram" not in html_css_lower
    assert "n8n" not in html_css_lower
    assert "isbn" not in lower
    assert "99187" not in html_css_lower


def test_tipadas_byte_exact_se_embutidas():
    html = _html()
    for name, expected in TIPADAS:
        path = ASSETS / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size == expected, (name, size, expected)
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", name
        assert f"assets/{name}" in html, name
    assert list(ASSETS.glob("*30PS*")) == []
    assert list(ASSETS.glob("*engineBay*")) == []
    assert not any((ASSETS).glob("*caixa8*cip1*"))
    assert html.count("<img") == 8


def test_gen_f3_f4_gaps_hold_ausente():
    html = _html()
    f3 = re.search(r'<section[^>]*id="gen-f3"[^>]*>(.*?)</section>', html, flags=re.S)
    assert f3
    assert "AUSENTE" in f3.group(1)
    assert "HOLD" in f3.group(1)
    assert "<img" not in f3.group(1).lower()
    f4 = re.search(r'<section[^>]*id="gen-f4"[^>]*>(.*?)</section>', html, flags=re.S)
    assert f4
    assert "AUSENTE" in f4.group(1)
    assert "Anchieta" in f4.group(1)
    assert "H1_VW_Beetle_1946" not in f4.group(1)
    assert "N0-A" in html
    assert "F-P0" in html


def test_gold_v11_tokens():
    css = CSS.read_text(encoding="utf-8")
    assert "#C9A227" in css
    assert "#0D0D0D" in css
    assert "#1A1A1A" in css
    assert "#F5F0E6" in css
    assert "montserrat" in css.lower()
    assert "inter" in css.lower()
    banned = (
        "#1b1b1b",
        "#ffffff",
        "#eeeae0",
        "#ececec",
        "#f6f4ee",
        "#5c5c5c",
        "#d6d6d6",
        "orange",
        "#e67e22",
        "#ff9800",
        "#f39c12",
    )
    lower = css.lower()
    for hex_or_name in banned:
        assert hex_or_name not in lower, hex_or_name
    assert not re.search(r"#fff\b", lower)


def test_legendas_cite_only_sem_drive_id():
    html = _html()
    caps = " ".join(_figcaptions(html))
    assert "drive.google.com" not in caps.lower()
    for did in (
        "1Kd6Y75J_Hczhb4CuG9R9mHOfTcf4AenT",
        "1vjVvZ18DYGUREYEfYFzvadlOa3OHGwbp",
        "1W9m0-CSUoeyLqDVafsEclQTNlUjV_qJZ",
        "1RJYn4YwIQmqERYNkpN8QMPVYu6LJYt1M",
        "1K2IIqdAtPPysoloSFJcmfuv43zr_AlqK",
        "12Xtkudi1r-gjmKmy1QTk9pjjmMTyZZtx",
        "1a_L6-bgoABwfW8VTeRfCA7nMg6zhUq_i",
        "1NQx1Ef7yG5O-uoU8JRjnc1RFfS3wChAi",
    ):
        assert did not in caps
    assert "Acervo" not in caps
    assert "Latas no lugar" in caps
    assert "KdF" in caps
