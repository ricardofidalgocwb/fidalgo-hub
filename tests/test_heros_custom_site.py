"""Guarda sites/heros-custom: MVP unpublished, NAP 439, sem promessas proibidas."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "heros-custom"
PAGES = [
    SITE / "index.html",
    SITE / "servicos" / "index.html",
    SITE / "prova" / "index.html",
    SITE / "como" / "index.html",
    SITE / "contato" / "index.html",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _all_html() -> str:
    return "\n".join(_read(p) for p in PAGES)


def test_artefatos_existem():
    assert (SITE / "css" / "site.css").is_file()
    assert (SITE / "js" / "site.js").is_file()
    assert (SITE / "README.md").is_file()
    for page in PAGES:
        assert page.is_file(), page


def test_unpublished_banner_e_pt_br():
    for page in PAGES:
        html = _read(page)
        assert 'lang="pt-BR"' in html
        assert "noindex" in html
        assert "UNPUBLISHED · DRAFT · Founder OK required to go live" in html
        assert "UNPUBLISHED · DRAFT" in html


def test_gold_v11_tokens():
    css = _read(SITE / "css" / "site.css").lower()
    assert "#c9a227" in css
    assert "#0d0d0d" in css
    assert "#1a1a1a" in css
    assert "#f5f0e6" in css


def test_cinco_ctas_e_jornada():
    home = _read(SITE / "index.html")
    servicos = _read(SITE / "servicos" / "index.html")
    como = _read(SITE / "como" / "index.html")
    for blob in (home, servicos):
        assert "Visita institucional" in blob
        assert "Vistoria / Passaporte Digital" in blob
        assert "Preventiva / corretiva" in blob
        assert "Clube / guarda" in blob
        assert "Vaga de curadoria" in blob
        assert "XLPE" in blob
        assert "Deutsch IP68" in blob
    for blob in (home, como):
        assert "Agendar" in blob
        assert "Vistoria" in blob
        assert "Execução" in blob
        assert "Entrega" in blob
        assert "Notion OS" in blob
        assert "Passaporte" in blob


def test_formulario_estatico():
    home = _read(SITE / "index.html")
    contato = _read(SITE / "contato" / "index.html")
    js = _read(SITE / "js" / "site.js")
    for blob in (home, contato):
        assert 'id="contato-form"' in blob
        assert 'name="nome"' in blob
        assert 'name="telefone"' in blob
        assert 'name="veiculo"' in blob
        assert 'name="servico"' in blob
        assert 'name="notas"' in blob
        assert "Fusca" in blob
        assert "Kombi" in blob
    assert "wa.me/5541991878091" in js
    assert "mailto:" in js
    assert "formspree" not in (home + contato + js).lower()
    assert "netlify" not in (home + contato + js).lower()


def test_nap_439_nao_557():
    blob = _all_html()
    assert "Olímio Monteiro Soares 439" in blob
    assert "Fanny" in blob
    assert "wa.me/5541991878091" in blob
    assert "(41) 99187-8091" in blob
    assert "heroscustomeletric@gmail.com" in blob
    for page in PAGES:
        html = _read(page)
        start = html.find('class="nap-block"')
        assert start != -1
        nap_block = html[start : start + 900]
        assert "557" not in nap_block
        assert "439" in nap_block
    home = _read(SITE / "index.html")
    assert "557" in home
    assert "contexto de clube" in home.lower()


def test_ia_cinco_itens_sem_clube_no_nav():
    for page in PAGES:
        html = _read(page)
        nav = html.split('aria-label="Principal"', 1)[1].split("</nav>", 1)[0]
        assert "Início" in nav or "Início" in html
        assert "Serviços" in nav
        assert "Prova" in nav
        assert "Como" in nav
        assert "Contato" in nav
        assert "Clube" not in nav


def test_proibidos_e_sem_metricas():
    html = _all_html()
    js = _read(SITE / "js" / "site.js")
    blob = html + js
    lower = blob.lower()
    assert "hotmart" not in lower or "sem n8n, hotmart" in lower
    assert "n8n" not in lower or "sem n8n" in lower
    assert "nft" not in lower
    assert "trello" in lower
    assert "não há trello como erp vivo" in lower or "nao ha trello como erp vivo" in lower
    assert "portal do cliente em 2026" in lower
    assert "login" in lower
    assert not re.search(r"\d+\s+vagas livres", lower)
    assert "sem métricas inventadas" in lower or "sem metricas inventadas" in lower
    assert "r$ 650" in lower
    assert "sujeita a vaga" in lower
    assert "3333-8644" not in html
    assert "99979-3395" not in html
    assert "BR 116" not in html and "BR-116" not in html


def test_css_js_sem_typo_box_sizing():
    css = _read(SITE / "css" / "site.css")
    assert "border-border-box" not in css
    assert "box-sizing: border-box" in css
