"""Guarda COM-PDF-APR-N0: Aprendiz unpublished, Gold v1.1, sem PII/nomes banidos."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACOTE = ROOT / "docs" / "propostas" / "COM-PDF-APR-N0"
HTML = PACOTE / "index.html"
README = PACOTE / "README.md"
CSS = PACOTE / "print.css"
PDF = PACOTE / "COM-PDF-APR-N0-aprendiz.pdf"


def _read(*paths: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in paths)


def _html() -> str:
    return HTML.read_text(encoding="utf-8")


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
    readme = README.read_text(encoding="utf-8")
    assert "não publicado" in readme.lower() or "nao publicado" in readme.lower()
    assert "aprendiz testa como aluno" in readme.lower()


def test_camada_a_indice_e_canon():
    html = _html()
    assert "Heros Custom" in html
    assert "Curso inicial elétrica simples (N0)" in html
    for aula in (
        "Energia zero e polaridade",
        "Ano + 6/12 V (1968)",
        "12 V ≠ alternador",
        "Diagrama do ano + foto da caixa",
        "Massas primeiro",
        "Multímetro parado",
    ):
        assert aula in html
    assert "1968" in html
    assert "1996" in html
    assert "03/01/1959" in html
    assert "18/11/1959" in html
    assert "12 V ≠ alternador" in html
    assert "energia zero → ano/tensão → geração → foto caixa" in html
    for q in ("A1", "A2", "A3", "A4", "A5", "A6"):
        assert q in html
    assert "Quiz D1" in html
    assert "fonte Notion Quiz D1 — gabarito na página editorial" in html
    assert "8/10" in html
    assert "~0 V" in html or "~0 V" in html.replace(" ", "")
    assert "NAP 439" in html or "439" in html
    assert "Não Eletro" in html or "não Eletro" in html


def test_camada_b_esqueleto():
    html = _html()
    assert "Só com Passaporte tipado" in html
    assert "B.1" in html
    assert "B.2" in html
    assert "B.3" in html
    assert "B.4" in html
    assert "B.5" in html
    assert "B.6" in html
    assert "Type 1 só" in html
    assert "67–81" in html
    assert "Proibido" in html or "proibido" in html.lower()
    assert "Sem SKU" in html or "sem SKU" in html.lower()
    assert html.lower().count("ausente") >= 3


def test_slots_ausentes_sem_img():
    html = _html()
    assert not re.search(r"<img\b", html, re.I)
    for slot in ("Caixa 8 pólos", "Caixa 12 pólos", "Dínamo vs alternador"):
        assert slot in html


def test_quiz_nao_inventa_dez_qa():
    html = _html()
    # Placeholder + regra. Não inventar 10 Q&A que se apresentem como cânon.
    assert "não inventa 10 perguntas" in html.lower() or "nao inventa 10 perguntas" in html.lower()
    assert not re.search(r"\b1B\s*·\s*2B\s*·\s*3B", html)


def test_proibido_pii_nomes_e_diagramas():
    blob = _read(HTML, CSS, README)
    html_css = _read(HTML, CSS)
    lower = blob.lower()
    assert "Theodoro" not in blob
    assert "Diogo" not in blob
    assert "AIW3138" not in blob
    assert "Herculid" not in blob
    assert "herculid" not in lower
    assert not re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", blob)
    html_css_lower = html_css.lower()
    assert "cpf" not in html_css_lower
    assert "notion.so" not in html_css_lower
    assert "notion.com" not in html_css_lower
    assert "instagram" not in html_css_lower
    assert "n8n" not in html_css_lower
    assert "R$" not in blob
    assert not re.search(r"diagrama da variant", lower)
    assert not re.search(r"usar o diagrama (do )?type\s*3", lower)
    assert not re.search(r"variant como diagrama", lower)
    assert not re.search(r"diagrama (de ensino )?(da |do )?(variant|type\s*3)", lower)


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
