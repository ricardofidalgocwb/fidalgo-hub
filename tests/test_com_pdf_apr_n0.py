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
    assert (PACOTE / "tests" / "README.md").is_file()
    assert (PACOTE / "TESTES.md").is_file()


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
    assert "vigia oval" in html
    assert "O que faz primeiro no negativo?" in html
    assert "1B · 2B · 3B · 4B · 5B · 6B · 7B · 8B · 9B · 10B" in html
    assert "~0 V" in html or "~0 V" in html.replace(" ", "")
    assert "Próximo: M1 chicote — ou agendar diagnóstico" in html
    assert "Não Eletro" in html or "não Eletro" in html
    assert "439" not in html
    assert "nap" not in html.lower()
    assert "99187" not in html
    assert "whatsapp" not in html.lower()
    assert not re.search(r"\(\s*41\s*\)", html)
    assert not re.search(r"\b\d{4,5}-?\d{4}\b", html)


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
    for slot in ("caixa 8 pólos", "caixa 12 pólos", "dínamo vs alternador"):
        assert slot in html.lower()
    assert html.lower().count("ausente") >= 3


def test_quiz_d1_editorial_e_a1_exato():
    html = _html()
    assert "vigia oval" in html
    assert "O que faz primeiro no negativo?" in html
    assert "Como medís parado?" in html
    assert "O que recusa num kit YT?" in html
    assert "1B · 2B · 3B · 4B · 5B · 6B · 7B · 8B · 9B · 10B" in html
    assert "ficha D1" in html


def test_cos_p0_quiz_sem_marca_gabarito_no_fim():
    html = _html()
    quiz = re.search(r'<ol class="quiz">(.*?)</ol>', html, re.S)
    assert quiz, "bloco Quiz D1 ausente"
    body = quiz.group(1)
    assert "✅" not in body
    assert "✔" not in body
    assert "✓" not in body
    css = CSS.read_text(encoding="utf-8")
    assert 'content: "○ "' in css or "content: '○ '" in css
    after = html[quiz.end() :]
    gabarito = "1B · 2B · 3B · 4B · 5B · 6B · 7B · 8B · 9B · 10B"
    assert gabarito in after
    assert gabarito not in html[: quiz.start()]
    assert 'id="gabarito-d1"' in after


def test_cos_p0_checklist_e_linhas_a1():
    html = _html()
    assert html.count("☐") >= 7
    assert html.count('class="write"') == 18
    assert "caixa 8 pólos" in html
    assert "caixa 12 pólos" in html
    assert "dínamo vs alternador" in html
    assert "Hold Founder/Ops" in html
    assert not re.search(r"<img\b", html, re.I)


def test_fichas_historico_h1_h3():
    html = _html()
    assert "Fichas-histórico (didáticas · anonimizadas)" in html
    assert "N0-H1" in html
    assert "N0-H2" in html
    assert "N0-H3" in html
    assert "H1 · Era B1 (1959–66)" in html
    assert "H2 · Era B2 (1967–69)" in html
    assert "H3 · Era B4 (1975–86)" in html
    assert "1200 / código B (slot AUSENTE)" in html
    assert "6 V medida" in html
    assert "pré-12 pólos / foto (slot 8 AUSENTE)" in html
    assert "dínamo 6 V (slot AUSENTE)" in html
    assert "Vigia retangular nacional" in html
    assert "E2 se misturar 12 V" in html
    assert "não misturar 12 V neste carro" in html
    assert "1300 / BF (1967 ainda pode 6 V)" in html
    assert "medir 6 ou 12 se ≥1968" in html
    assert "foto 8 vs 12 sem inventar boletim (AUSENTE)" in html
    assert "dínamo 12 V comum se 12 V ≠ alt automático" in html
    assert "“12 V=1967” recusar" in html or '"12 V=1967" recusar' in html
    assert "cânon 1968" in html
    assert "1967 ≠ 12 V automático" in html
    assert "1600 BB (prefixo slot AUSENTE)" in html
    assert "12 V medida" in html
    assert "≥1975 = 12 pólos só se foto confirmar (AUSENTE)" in html
    assert "dínamo ou alt — duas OS" in html
    assert "Fafá possível 79–86" in html
    assert "não data sozinha" in html
    assert "Massa ~0 V N0" in html
    assert "não pede dínamo→alt como se fosse 6→12" in html
    assert html.count("☐ Aluno") >= 3
    assert html.count("Selo domínio") == 3
    assert "caixa 8 pólos" in html
    assert "caixa 12 pólos" in html
    assert "dínamo vs alternador" in html
    assert html.lower().count("ausente") >= 6
    assert not re.search(r"<img\b", html, re.I)
    quiz = re.search(r'<ol class="quiz">(.*?)</ol>', html, re.S)
    assert quiz and "✅" not in quiz.group(1)
    assert "Próximo: M1 chicote — ou agendar diagnóstico" in html
    assert "439" not in html
    assert "nap" not in html.lower()
    assert "whatsapp" not in html.lower()
    assert "Theodoro" not in html
    assert "Diogo" not in html
    assert not re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", html)
    assert not re.search(r"diagrama da variant", html.lower())
    assert not re.search(r"usar o diagrama (do )?type\s*3", html.lower())


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
    assert "whatsapp" not in html_css_lower
    assert "99187" not in html_css_lower
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
