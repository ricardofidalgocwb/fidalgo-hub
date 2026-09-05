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


def _slot(html: str, heading: str) -> str:
    m = re.search(
        rf'<div class="slot[^"]*">\s*<div>\s*<h3>{re.escape(heading)}</h3>.*?</div>\s*(?:<div class="contrast-pair">.*?</div>|<figure>.*?</figure>|<p>.*?</p>)(?:\s*<p class="cite-secondary">.*?</p>)?\s*</div>',
        html,
        flags=re.S,
    )
    assert m, f"slot {heading!r} não encontrado"
    return m.group(0)


def test_slot_a8_drive_dinam_alt_contrast():
    html = _html()
    dinam = PACOTE / "assets" / "N0_A8_dinam_SRC-heritagestocks.jpg"
    alt = PACOTE / "assets" / "N0_A8_alt_SRC-appletreekit.jpg"
    commons = PACOTE / "assets" / "N0_A8_engineGenAlt_SRC-commons.jpg"
    assert dinam.is_file()
    assert alt.is_file()
    assert commons.is_file()
    assert dinam.stat().st_size >= 100_000
    assert alt.stat().st_size >= 100_000
    assert dinam.stat().st_size == 443_360
    assert alt.stat().st_size == 141_153
    assert dinam.read_bytes()[:3] == b"\xff\xd8\xff"
    assert alt.read_bytes()[:3] == b"\xff\xd8\xff"
    geracao = _slot(html, "dínamo vs alternador")
    assert geracao.count("<img") == 2
    assert "assets/N0_A8_dinam_SRC-heritagestocks.jpg" in geracao
    assert "assets/N0_A8_alt_SRC-appletreekit.jpg" in geracao
    assert "assets/N0_A8_engineGenAlt_SRC-commons.jpg" not in re.search(
        r'<div class="contrast-pair">(.*?)</div>', geracao, flags=re.S
    ).group(1)
    assert "heritagestocks" in geracao
    assert "appletreekit" in geracao
    assert "Ausente" not in geracao
    assert "AUSENTE" not in geracao
    assert "A.8" in geracao
    assert "Drive" in geracao
    assert "secundário" in geracao.lower() or "secundario" in geracao.lower()
    assert "N0_A8_engineGenAlt_SRC-commons.jpg" in geracao
    assert "Wikimedia Commons" in geracao
    caixa8 = _slot(html, "caixa 8 pólos")
    caixa12 = _slot(html, "caixa 12 pólos")
    caixa8_asset = PACOTE / "assets" / "N0_caixa8_fuseBox8polos_SRC-appletree.jpg"
    assert caixa8_asset.is_file()
    assert caixa8_asset.stat().st_size >= 100_000
    assert re.search(r"<img\b", caixa8, re.I)
    assert "assets/N0_caixa8_fuseBox8polos_SRC-appletree.jpg" in caixa8
    assert "Ausente" not in caixa8
    assert "AUSENTE" not in caixa8
    assert "appletreeauto 61–66 (Acervo)" in caixa8
    assert "appletree" in caixa8.lower()
    assert "N0_caixa8_fuseBox8polos_SRC-cip1" not in caixa8
    assert "SRC-appletree" in caixa8
    caixa12_asset = PACOTE / "assets" / "N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg"
    assert caixa12_asset.is_file()
    assert caixa12_asset.stat().st_size >= 100_000
    assert re.search(r"<img\b", caixa12, re.I)
    assert "assets/N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg" in caixa12
    assert "Ausente" not in caixa12
    assert "AUSENTE" not in caixa12
    assert "cip1.com/vwc-111-937-505-m" in caixa12
    assert html.lower().count("ausente") >= 3
    assert "Cap2_engine1962" not in html
    assert "M6_T_engineBayTin" not in html
    assert "getriebe" not in html.lower()
    assert "explosionsmodell" not in html.lower()
    assert not any((PACOTE / "assets").glob("*caixa8*cip1*"))
    assert not (PACOTE / "assets" / "N0_caixa8_fuseBox8polos_SRC-cip1.jpg").exists()
    assert not any((PACOTE / "assets").glob("*getriebe*"))
    assert not any((PACOTE / "assets").glob("*explosionsmodell*"))
    assert html.count("<img") == 4


def test_slot_caixa12_cip1_e_caixa8_appletree():
    html = _html()
    asset12 = PACOTE / "assets" / "N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg"
    asset8 = PACOTE / "assets" / "N0_caixa8_fuseBox8polos_SRC-appletree.jpg"
    assert asset12.is_file()
    assert asset8.is_file()
    assert asset12.stat().st_size >= 100_000
    assert asset8.stat().st_size >= 100_000
    caixa12 = _slot(html, "caixa 12 pólos")
    assert "N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg" in caixa12
    assert "www2.cip1.com/vwc-111-937-505-m" in caixa12
    caixa8 = _slot(html, "caixa 8 pólos")
    assert "N0_caixa8_fuseBox8polos_SRC-appletree.jpg" in caixa8
    assert "appletreeauto 61–66 (Acervo)" in caixa8
    assert "appletree" in caixa8.lower()
    assert "N0_caixa8_fuseBox8polos_SRC-cip1" not in caixa8
    assert "N0_caixa8_fuseBox8polos_SRC-cip1" not in html
    geracao = _slot(html, "dínamo vs alternador")
    assert "N0_A8_dinam_SRC-heritagestocks.jpg" in geracao
    assert "N0_A8_alt_SRC-appletreekit.jpg" in geracao
    assert "heritagestocks" in geracao
    assert "appletreekit" in geracao


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
    assert html.count("<img") == 4
    assert "assets/N0_A8_dinam_SRC-heritagestocks.jpg" in html
    assert "assets/N0_A8_alt_SRC-appletreekit.jpg" in html
    assert "assets/N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg" in html
    assert "assets/N0_caixa8_fuseBox8polos_SRC-appletree.jpg" in html


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
    assert html.count("<img") == 4
    assert "assets/N0_A8_dinam_SRC-heritagestocks.jpg" in html
    assert "assets/N0_A8_alt_SRC-appletreekit.jpg" in html
    assert "assets/N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg" in html
    assert "assets/N0_caixa8_fuseBox8polos_SRC-appletree.jpg" in html
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
