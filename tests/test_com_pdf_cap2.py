"""Guarda COM-PDF-CAP2-motor: Cap.2 unpublished, Gold v1.1, sem PII/canais proibidos."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACOTE = ROOT / "docs" / "propostas" / "COM-PDF-CAP2-motor"
HTML = PACOTE / "index.html"
README = PACOTE / "README.md"
CSS = PACOTE / "print.css"
PDF = PACOTE / "COM-PDF-CAP2-motor.pdf"


def _read(*paths: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in paths)


def _html() -> str:
    return HTML.read_text(encoding="utf-8")


def _miolo(html: str) -> str:
    """Anatomia §§1–5 only — before checklist / item 9 / quiz."""
    start = html.find("<h2>1. O que é o motor do Type 1</h2>")
    end = html.find("<h2>6. Checklist Aprendiz")
    assert start != -1 and end != -1 and end > start
    return html[start:end]


def _quiz_options_blob(html: str) -> str:
    """Texto das alternativas do quiz, sem o bloco de gabarito."""
    m = re.search(
        r'class="quiz"(.*?)Gabarito',
        html,
        flags=re.S | re.I,
    )
    assert m, "bloco .quiz antes do gabarito não encontrado"
    return m.group(1)


def test_artefatos_existem():
    assert HTML.is_file()
    assert README.is_file()
    assert CSS.is_file()
    assert (PACOTE / "emitir-pdf.sh").is_file()
    assert PDF.is_file()
    assert PDF.stat().st_size > 10_000


def test_nao_publicado_e_pt_br():
    html = _html()
    assert 'lang="pt-BR"' in html
    assert "noindex" in html
    assert "NÃO PUBLICADO" in html or "Não publicar" in html
    assert "sem site até OK Founder" in html or "sem site até ok founder" in html.lower()
    assert "rascunho 0.2" in html.lower()
    readme = README.read_text(encoding="utf-8")
    assert "não publicado" in readme.lower() or "nao publicado" in readme.lower()
    assert "separado" in readme.lower()
    assert "com-pdf-apr-n0" in readme.lower()


def test_capa_e_miolo_acervo():
    html = _html()
    assert "Heros Custom" in html
    assert "Cap. 2 — Anatomia do motor boxer a ar" in html
    assert "Type 1" in html
    assert "4" in html or "Quatro" in html
    assert "opostos" in html.lower()
    assert "comando no bloco" in html.lower()
    assert "1-4-3-2" in html
    assert "tinware" in html.lower()
    assert "ventoinha" in html.lower()
    assert "aletas" in html.lower()
    assert "lubrifica" in html.lower() and "tira calor" in html.lower()
    assert "ficha D1" in html or "D1" in html
    assert "foto do prefixo" in html.lower() or "foto prefixo" in html.lower()
    assert "1968" in html
    assert "12 V ≠ alternador" in html or "12 V ≠ alt" in html or "12 V ≠ alternador" in html
    assert "Cap.14" in html or "Cap. 14" in html
    assert "N0" in html


def test_spec_table_somente_acervo():
    html = _html()
    assert "1192" in html
    assert "1285" in html
    assert "1493" in html
    assert "1584" in html
    assert "6,6" in html
    assert "7,2" in html
    assert "1967" in html
    assert "ago/1970" in html
    assert "set/1974" in html
    assert "abr/1975" in html
    assert "1993–96" in html or "1993-96" in html
    assert "Itamar" in html
    for codigo in ("B", "BF", "BH", "BB", "BD"):
        assert codigo in html
    assert "BA" in html and "BN" in html and "Brasília" in html
    assert "BV" in html and "Variant" in html
    assert "BL" in html and "1678" in html and "SP2" in html
    html_l = html.lower()
    assert "não são type 1" in html_l or "nao sao type 1" in html_l
    assert "sem cv" in html_l
    assert " cv" not in html_l.replace("sem cv", "")
    assert not re.search(r"\b\d+\s*cv\b", html_l)
    assert "nm" not in html_l
    assert "kgfm" not in html_l
    assert "kgf" not in html_l
    assert "ω" not in html_l and "ohm" not in html_l
    assert not re.search(r"\b\d+[,\.]?\d*\s*(mm|nm)\b", html_l)


def test_checklist_8_e_selo():
    html = _html()
    for item in (
        "Ventoinha",
        "Tinware",
        "Aletas",
        "Óleo",
        "Termostato",
        "prefixo",
        "1-4-3-2",
        "Carb",
        "BD",
    ):
        assert item.lower() in html.lower() or item in html
    assert "8 ☐" in html or "8 ☐" in html.replace(" ", "")
    assert "não misturou n0 no miolo" in html.lower() or "nao misturou n0 no miolo" in html.lower()
    assert "item 9" in html.lower()
    assert "N0 only" in html or "só ponte" in html.lower() or "nao miolo" in html.lower()


def test_quiz_literais_sem_check_nas_opcoes():
    html = _html()
    assert "nomeie a peça" in html.lower()
    assert "Latas + aletas + ventoinha" in html
    assert "Tinware / latas" in html
    assert "1-4-3-2" in html
    assert "Foto do prefixo" in html
    assert "Lubrifica e tira calor" in html
    assert "Controla fluxo a frio" in html
    assert "N0 / Cap.14" in html
    assert "Não fecha" in html
    assert "1A · 2A · 3B · 4B · 5A · 6B · 7B · 8B · 9B · 10B" in html
    opcoes = _quiz_options_blob(html)
    assert "✅" not in opcoes
    assert "✔" not in opcoes
    assert "✓" not in opcoes
    gabarito_idx = html.lower().rfind("gabarito")
    assert gabarito_idx > html.lower().find("quiz")
    assert "1A · 2A · 3B · 4B · 5A · 6B · 7B · 8B · 9B · 10B" in html[gabarito_idx:]


def test_slots_ausentes_sem_img():
    html = _html()
    assert not re.search(r"<img\b", html, re.I)
    for slot in (
        "Tinware completo",
        "Prefixo bloco",
        "Ventoinha",
    ):
        assert slot in html
    assert html.lower().count("ausente") >= 3


def test_proibido_pii_nomes_preco_isbn_canais():
    blob = _read(HTML, CSS, README)
    html_css = _read(HTML, CSS)
    lower = blob.lower()
    html_css_lower = html_css.lower()

    assert "Theodoro" not in blob
    assert "Herculid" not in blob
    assert "herculid" not in lower
    assert not re.search(r"curso\s+h[eé]rcules", blob, re.I)
    assert "Type 1 Variant" not in blob
    assert "Variant Type 1" not in blob
    assert not re.search(r"variant como type\s*1", lower)
    assert not re.search(r"variant as type\s*1", lower)

    assert "ISBN" not in blob
    assert "isbn" not in lower
    assert "R$" not in blob
    assert "preço" not in html_css_lower
    assert not re.search(r"\bpreco\b", html_css_lower)
    assert "publish" not in html_css_lower.replace("unpublished", "")

    assert "NAP" not in html_css
    assert not re.search(r"\b439\b", html_css)
    assert "whatsapp" not in html_css_lower
    assert not re.search(r"\(\d{2}\)\s*\d{4,5}-?\d{4}", html_css)
    assert not re.search(r"\b9\d{4}-?\d{4}\b", html_css)

    assert not re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", blob)
    assert "cpf" not in html_css_lower
    assert "notion.so" not in html_css_lower
    assert "notion.com" not in html_css_lower
    assert "instagram" not in html_css_lower
    assert "n8n" not in html_css_lower


def test_nao_mistura_n0_no_miolo():
    html = _html()
    assert "Curso inicial elétrica simples (N0)" not in html
    assert "Quiz D1" not in html
    assert "vigia oval" not in html.lower()
    assert "A1" not in html or "1A" in html
    for aula in (
        "Energia zero e polaridade",
        "Massas primeiro",
        "Multímetro parado",
    ):
        assert aula not in html


def test_tec_gates_miolo_sem_torque_pn_folga_n0():
    html = _html()
    miolo = _miolo(html)
    miolo_l = miolo.lower()
    assert "torque" not in miolo_l
    assert "folga" not in miolo_l
    assert not re.search(r"\bpn\b", miolo_l)
    assert "ω" not in miolo_l and "ohm" not in miolo_l
    assert "item 9" not in miolo_l
    assert "tensão medida" not in miolo_l
    assert "foto da caixa" not in miolo_l
    assert "12 v ≠ alternador" not in miolo_l
    after = html[html.find("<h2>6. Checklist Aprendiz") :]
    assert "Item 9" in after
    assert "N0 only" in after
    assert "tensão medida" in after.lower() or "tensão + caixa" in after.lower()
    assert "Type 3 = outro módulo" in html
    assert not re.search(r"diagrama (do |da )?type\s*3", html, re.I)
    assert "✅" not in _quiz_options_blob(html)


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
