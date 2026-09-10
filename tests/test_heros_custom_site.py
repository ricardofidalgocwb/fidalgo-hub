"""ENT gates — Founder OK MVP unpublished (Heros Custom).

Locks:
- 5 CTAs: visita · vistoria/Passaporte · preventiva · Clube/guarda · vaga curadoria
- NAP Heros: Olímio Monteiro Soares 439 · WhatsApp (41) 99187-8091 · Gold #C9A227
- Do NOT invent free parking slots (Vagas DB empty)
- No publish / no n8n Active / no Hotmart go-live
- Separate from Cap.2 tinware
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "heros-custom"
CAP2 = ROOT / "docs" / "propostas" / "COM-PDF-CAP2-motor"
PAGES = [
    SITE / "index.html",
    SITE / "servicos" / "index.html",
    SITE / "prova" / "index.html",
    SITE / "como" / "index.html",
    SITE / "contato" / "index.html",
]

CTAS = (
    ("visita-institucional", "Visita institucional"),
    ("vistoria-passaporte", "Vistoria / Passaporte Digital"),
    ("preventiva-corretiva", "Preventiva / corretiva"),
    ("clube-guarda", "Clube / guarda"),
    ("vaga-curadoria", "Vaga de curadoria"),
)

SLOT_COUNT_RE = re.compile(
    r"""
    (?:\d+\s+vagas?\s+livres)
    | (?:vagas?\s+livres\s*[:=]\s*\d+)
    | (?:\d+\s+vagas?\s+(?:de\s+)?(?:guarda|estacionamento|parking))
    | (?:estacionamento\s+livre)
    | (?:há\s+\d+\s+vagas)
    | (?:ha\s+\d+\s+vagas)
    """,
    re.I | re.X,
)


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


def test_gold_c9a227():
    css = _read(SITE / "css" / "site.css")
    assert "#C9A227" in css or "#c9a227" in css
    assert re.search(r"--gold:\s*#c9a227", css, re.I)
    assert "#C9A227" in _read(SITE / "README.md")


def test_cinco_ctas_exactas():
    home = _read(SITE / "index.html")
    servicos = _read(SITE / "servicos" / "index.html")
    contato = _read(SITE / "contato" / "index.html")
    js = _read(SITE / "js" / "site.js")
    for slug, label in CTAS:
        for blob in (home, servicos, contato, js):
            assert slug in blob, slug
        for blob in (home, servicos, contato):
            assert label in blob, label
    for blob in (home, servicos):
        assert "XLPE" in blob
        assert "Deutsch IP68" in blob
    for html in (home, contato):
        options = [
            value
            for value in re.findall(
                r'<option value="([^"]*)">',
                html[html.find('id="servico"') : html.find("</select>", html.find('id="servico"'))],
            )
            if value
        ]
        assert options == [slug for slug, _label in CTAS], options


def test_jornada_quatro_passos():
    home = _read(SITE / "index.html")
    como = _read(SITE / "como" / "index.html")
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


def test_nap_439_whatsapp_99187():
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
        assert "99187-8091" in nap_block
        assert "wa.me/5541991878091" in nap_block
    home = _read(SITE / "index.html")
    assert "557" in home
    assert "contexto de clube" in home.lower()


def test_ia_cinco_itens_sem_clube_no_nav():
    for page in PAGES:
        html = _read(page)
        nav = html.split('aria-label="Principal"', 1)[1].split("</nav>", 1)[0]
        assert "Início" in nav
        assert "Serviços" in nav
        assert "Prova" in nav
        assert "Como" in nav
        assert "Contato" in nav
        assert "Clube" not in nav


def test_nao_inventa_vagas_livres():
    blob = _all_html() + _read(SITE / "js" / "site.js") + _read(SITE / "README.md")
    lower = blob.lower()
    assert SLOT_COUNT_RE.search(blob) is None
    assert "não inventa vagas livres" in lower or "nao inventa vagas livres" in lower
    assert "sujeita a vaga" in lower
    assert "r$ 650" in lower


def test_sem_publish_n8n_active_hotmart_golive():
    html = _all_html()
    js = _read(SITE / "js" / "site.js")
    lower = (html + js).lower()
    assert "n8n active" not in lower
    assert "sem n8n" in lower
    assert "hotmart" in lower
    assert "sem n8n, hotmart" in lower
    assert "founder ok required to go live" in lower
    assert "nft" not in lower
    assert "não há trello como erp vivo" in lower or "nao ha trello como erp vivo" in lower
    assert "portal do cliente em 2026" in lower
    assert "3333-8644" not in html
    assert "99979-3395" not in html
    assert "BR 116" not in html and "BR-116" not in html
    assert not (SITE / "netlify.toml").exists()
    assert not (SITE / ".netlify").exists()


def test_separado_do_cap2_tinware():
    site_blob = _all_html() + _read(SITE / "css" / "site.css") + _read(SITE / "js" / "site.js")
    assert "Cap2_P0_tinware" not in site_blob
    assert "COM-PDF-CAP2" not in site_blob
    assert "AUR1500" not in site_blob
    assert "coccinelle" not in site_blob.lower()
    if CAP2.is_dir():
        cap2_html = CAP2 / "index.html"
        if cap2_html.is_file():
            assert "sites/heros-custom" not in _read(cap2_html)


def test_css_js_sem_typo_box_sizing():
    css = _read(SITE / "css" / "site.css")
    assert "border-border-box" not in css
    assert "box-sizing: border-box" in css
