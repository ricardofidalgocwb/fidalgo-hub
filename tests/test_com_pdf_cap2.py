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
    assert not re.search(r"\bnm\b", html_l)
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
    block = re.search(r'<ol class="checklist">(.*?)</ol>', html, flags=re.S)
    assert block, "ol.checklist não encontrado"
    lis = re.findall(r"<li\b[^>]*>(.*?)</li>", block.group(1), flags=re.S)
    assert len(lis) == 8
    for li in lis:
        assert "☐" in li
    gate = re.search(
        r'<p class="gate">\s*<strong>Item 9.*?</p>',
        html,
        flags=re.S,
    )
    assert gate, "gate Item 9 não encontrado"
    assert "☐" not in gate.group(0)


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


def _slot(html: str, heading: str) -> str:
    m = re.search(
        rf'<div class="slot[^"]*">\s*<div>\s*<h3>{re.escape(heading)}</h3>(.*?)</div>\s*(?:<figure>.*?</figure>|<p>.*?</p>)\s*</div>',
        html,
        flags=re.S,
    )
    assert m, f"slot {heading!r} não encontrado"
    return m.group(0)


def test_slot_tinware_commons_demais_ausentes():
    html = _html()
    asset = PACOTE / "assets" / "Cap2_engineBay_SRC-commons.jpg"
    assert asset.is_file()
    assert asset.stat().st_size >= 100_000
    tinware = _slot(html, "Tinware completo (didático)")
    assert re.search(r"<img\b", tinware, re.I)
    assert "assets/Cap2_engineBay_SRC-commons.jpg" in tinware
    assert "Ausente" not in tinware
    assert "AUSENTE" not in tinware
    assert "Wikimedia Commons" in tinware
    assert "SRC-commons" in tinware
    prefixo = _slot(html, "Prefixo bloco B/BF/BH/BB/BD")
    ventoinha = _slot(html, "Ventoinha / correia")
    assert "Ausente" not in prefixo
    assert "Ausente" not in ventoinha
    assert re.search(r"<img\b", prefixo, re.I)
    assert re.search(r"<img\b", ventoinha, re.I)
    assert "assets/Cap2_P0_prefixBD_crop_SRC-commons.jpg" in prefixo
    assert "assets/Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg" in ventoinha
    assert html.lower().count("ausente") >= 1
    assert "stamp b" in html.lower() and "AUSENTE" in html
    assert "M6_T_engineBayTin" not in html
    assert "Cap2_engine1962" not in html
    assert html.count("<img") == 8
    assert html.count("assets/Cap2_engineBay_SRC-commons.jpg") == 1
    aur = _slot(html, "Tinware completo (AUR1500)")
    cocc = _slot(html, "Tinware completo (Coccinelle)")
    avi = _slot(html, "Tinware terciário (1965AVI)")
    assert re.search(r"<img\b", aur, re.I)
    assert re.search(r"<img\b", cocc, re.I)
    assert re.search(r"<img\b", avi, re.I)
    assert "assets/Cap2_P0_tinware_AUR1500_SRC-commons.jpg" in aur
    assert "assets/Cap2_P0_tinware_coccinelle_SRC-commons.jpg" in cocc
    assert "assets/Cap2_P0_tinware_1965AVI_SRC-commons.jpg" in avi
    assert "Ausente" not in aur and "AUSENTE" not in aur
    assert "Ausente" not in cocc and "AUSENTE" not in cocc
    assert "Ausente" not in avi and "AUSENTE" not in avi
    assert "Wikimedia Commons" in aur and "Wikimedia Commons" in cocc
    assert "aftermarket" in avi.lower()
    assert "p1 opcional" in avi.lower() or "terciár" in avi.lower()


def test_p0_prefixbd_pass_pair_sem_stamp_a():
    assets = PACOTE / "assets"
    crop = assets / "Cap2_P0_prefixBD_crop_SRC-commons.jpg"
    fan = assets / "Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg"
    tin = assets / "Cap2_engineBay_SRC-commons.jpg"
    html = _html()
    readme = README.read_text(encoding="utf-8")
    assert crop.is_file() and fan.is_file()
    assert crop.stat().st_size == 241_948
    assert fan.stat().st_size == 708_229
    assert crop.read_bytes()[:3] == b"\xff\xd8\xff"
    assert fan.read_bytes()[:3] == b"\xff\xd8\xff"
    assert tin.read_bytes() != crop.read_bytes()
    assert tin.read_bytes() != fan.read_bytes()
    assert list(assets.glob("*prefixA*")) == []
    assert list(assets.glob("*HOLD_rimA*")) == []
    assert list(assets.glob("Cap2_P0_prefixB_*")) == []
    assert {p.name for p in assets.glob("Cap2_P0_prefixBD_*")} == {
        "Cap2_P0_prefixBD_crop_SRC-commons.jpg",
        "Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg",
    }
    assert not any(
        p.stat().st_size not in {241_948, 708_229} for p in assets.glob("Cap2_P0_prefixBD_*")
    )
    assert "Cap2_P0_prefixBD_crop_SRC-commons.jpg" in html
    assert "Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg" in html
    assert "1EPi6wjWdL1lYai71eafFt8xQ7eD6NDqc" in html
    assert "1jmhGbNjFbjrm5UpbaEZWXd1UwiLHEB7r" in html
    assert "1EPi6wjWdL1lYai71eafFt8xQ7eD6NDqc" in readme
    assert "1jmhGbNjFbjrm5UpbaEZWXd1UwiLHEB7r" in readme
    assert "241948" in readme
    assert "708229" in readme
    assert "label BD" in html.lower() or "commons · bd" in html.lower()
    assert "stamp A" not in html.lower()
    assert "prefixa" not in html.lower()
    assert "1bWAvwvwzPQFRLmPWGjVDtHeizJTGhTIc" not in html
    assert "1rgEg7oxpCreZpA42juxU0bSIpVBfRlb-" not in html
    assert html.count("<img") == 8


def test_p0_tinware_aur_cocc_exact_sizes_sem_30ps():
    assets = PACOTE / "assets"
    aur = assets / "Cap2_P0_tinware_AUR1500_SRC-commons.jpg"
    cocc = assets / "Cap2_P0_tinware_coccinelle_SRC-commons.jpg"
    tin = assets / "Cap2_engineBay_SRC-commons.jpg"
    html = _html()
    readme = README.read_text(encoding="utf-8")
    assert aur.is_file() and cocc.is_file() and tin.is_file()
    assert aur.stat().st_size == 483_449
    assert cocc.stat().st_size == 1_111_977
    assert tin.stat().st_size == 193_513
    assert aur.read_bytes()[:3] == b"\xff\xd8\xff"
    assert cocc.read_bytes()[:3] == b"\xff\xd8\xff"
    assert tin.read_bytes() != aur.read_bytes()
    assert tin.read_bytes() != cocc.read_bytes()
    assert aur.read_bytes() != cocc.read_bytes()
    assert list(assets.glob("*30PS*")) == []
    assert list(assets.glob("*1Cmt8*")) == []
    names = [p.name for p in assets.iterdir() if p.is_file()]
    assert not any("30PS" in n for n in names)
    assert not any("1Cmt8" in n for n in names)
    assert "Cap2_P0_tinware_AUR1500_SRC-commons.jpg" in html
    assert "Cap2_P0_tinware_coccinelle_SRC-commons.jpg" in html
    assert "1W9m0-CSUoeyLqDVafsEclQTNlUjV_qJZ" in html
    assert "1RJYn4YwIQmqERYNkpN8QMPVYu6LJYt1M" in html
    assert "Engine_of_VW_1500_AUR_131F" in html
    assert "Volkswagen_Coccinelle" in html
    assert "1W9m0-CSUoeyLqDVafsEclQTNlUjV_qJZ" in readme
    assert "1RJYn4YwIQmqERYNkpN8QMPVYu6LJYt1M" in readme
    assert "483449" in readme
    assert "1111977" in readme
    assert "Engine_of_VW_1500_AUR_131F" in readme
    assert "Volkswagen_Coccinelle" in readme
    assert "stamp b" in html.lower()
    assert "stamp b" in readme.lower()
    assert "AUSENTE" in html and "AUSENTE" in readme
    assert "1Cmt8" not in html
    assert "30PS" not in html
    assert html.count("assets/Cap2_engineBay_SRC-commons.jpg") == 1
    assert html.count("<img") == 8
    avi = assets / "Cap2_P0_tinware_1965AVI_SRC-commons.jpg"
    assert avi.is_file()
    assert avi.stat().st_size == 409_825
    assert avi.read_bytes()[:3] == b"\xff\xd8\xff"
    assert avi.read_bytes() != aur.read_bytes()
    assert avi.read_bytes() != cocc.read_bytes()
    assert avi.read_bytes() != tin.read_bytes()
    assert "Cap2_P0_tinware_1965AVI_SRC-commons.jpg" in html
    assert "19ynmIA_YGOpj83VNV4ngahL6QGgKYSnH" in html
    assert "AVI2387" in html
    assert "19ynmIA_YGOpj83VNV4ngahL6QGgKYSnH" in readme
    assert "409825" in readme
    assert "AVI2387" in readme
    assert html.find("Cap2_P0_tinware_AUR1500_SRC-commons.jpg") < html.find(
        "Cap2_P0_tinware_1965AVI_SRC-commons.jpg"
    )
    assert html.find("Cap2_P0_tinware_coccinelle_SRC-commons.jpg") < html.find(
        "Cap2_P0_tinware_1965AVI_SRC-commons.jpg"
    )
    assert "primário" in html.lower() and "terciár" in html.lower()
    assert "aftermarket" in html.lower()
    assert "não substitui" in html.lower() or "nao substitui" in html.lower()
    assert html.count("assets/Cap2_P0_tinware_1965AVI_SRC-commons.jpg") == 1


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


def test_p1_mito_correcao_seis_linhas():
    html = _html()
    start = html.find("<h3>Mito × correção</h3>")
    end = html.find("<h2>2. Por que esquenta e por que vaza</h2>")
    assert start != -1 and end != -1 and end > start
    table = html[start:end]
    rows = (
        (
            "«É ar = não precisa de lata»",
            "Sem tinware o fluxo foge; kit aftermarket costuma omitir defletores — não fecha orçamento de motor.",
        ),
        (
            "«Tira o termostato/anel pra render»",
            "Termostato/anel (quando presente) controla fluxo a frio — não «tira pra render».",
        ),
        (
            "«Cilindrada do CRLV = motor de hoje»",
            "Data o carro pela ficha D1; o motor pela foto do prefixo no bloco (B/BF/BH/BB/BD…).",
        ),
        (
            "«Óleo só lubrifica»",
            "No Type 1 a ar o óleo lubrifica e tira calor.",
        ),
        (
            "«Cap.2 resolve elétrica»",
            "Tensão + caixa + gerador = N0. Cap.2 = tinware / ar / prefixo.",
        ),
        (
            "«Sem foto do bloco fecha OS de motor»",
            "Sem tinware completo + sem foto do prefixo = não fecha.",
        ),
    )
    assert table.count("<tr>") == 7
    for mito, correcao in rows:
        assert mito in table
        assert correcao in table
    assert "Correção Heros" in table
    assert "✅" not in table
    assert html.count("<img") == 8
    assert "Cap2_engine1962" not in html
    assert "M6_T_engineBayTin" not in html
    assert "Cap2_P0_prefixBD_crop_SRC-commons.jpg" in html[start:end]
    prefixo = _slot(html, "Prefixo bloco B/BF/BH/BB/BD")
    ventoinha = _slot(html, "Ventoinha / correia")
    assert "Ausente" not in prefixo
    assert "Ausente" not in ventoinha
    assert re.search(r"<img\b", prefixo, re.I)
    assert re.search(r"<img\b", ventoinha, re.I)


def test_interativo_p1_write_e_perguntas_abertas():
    html = _html()
    css = CSS.read_text(encoding="utf-8")
    assert ".write" in css
    assert "border-bottom" in css
    assert html.count('class="write"') == 4
    assert html.count('class="write" aria-hidden="true"') == 4
    assert (
        "Aponte no bay: prefixo no bloco · ventoinha/correia · 1 lata que"
        in html
    )
    assert "fecha o fluxo · aletas visíveis." in html
    motor = re.search(
        r"<td>\s*Motor\s*</td>\s*<td>(.*?)</td>",
        html,
        flags=re.S,
    )
    assert motor, "célula Motor da ponte não encontrada"
    assert 'class="write"' in motor.group(1)
    assert "Aponte no bay" in motor.group(1)
    abertas = re.search(
        r'class="qblock"[^>]*aria-labelledby="cap2-abertas"(.*?)</section>',
        html,
        flags=re.S,
    )
    assert abertas, "subsecção perguntas abertas não encontrada"
    bloco = abertas.group(1)
    assert "Perguntas abertas" in bloco
    qs = (
        "Qual letra de família lês no prefixo do bloco, e por que o ano do CRLV não data o motor sozinho?",
        "Sem uma lata no lugar, o que o ar faz em vez de passar nas aletas — e o que isso tem a ver com superaquecimento?",
        "Em uma frase: correia → ventoinha → latas → aletas; onde o óleo entra como agente térmico (não só lubrificante)?",
    )
    for q in qs:
        assert q in re.sub(r"\s+", " ", bloco)
    assert bloco.count('class="write"') == 3
    novo = motor.group(1) + bloco
    novo_l = novo.lower()
    assert "Ω" not in novo
    assert "ω" not in novo_l
    assert "ohm" not in novo_l
    assert "torque" not in novo_l
    assert "crimp" not in novo_l
    assert not re.search(r"\bpn\b", novo_l)
    quiz_idx = html.find('class="quiz"')
    gabarito_idx = html.lower().rfind("gabarito")
    assert quiz_idx != -1 and gabarito_idx > quiz_idx
    assert html.find('id="cap2-abertas"') < quiz_idx
    assert "1A · 2A · 3B · 4B · 5A · 6B · 7B · 8B · 9B · 10B" in html[gabarito_idx:]
    assert "✅" not in _quiz_options_blob(html)


def test_tec_soft_write3q_identificacao_sem_torque_sem_eletrica_prova():
    """TEC PASS soft: no torque in miolo; elétrica = N0 handoff; write+3Q = ID only."""
    html = _html()
    miolo = _miolo(html)
    miolo_l = miolo.lower()
    assert "torque" not in miolo_l
    assert "folga" not in miolo_l
    assert "Perguntas abertas" in miolo
    assert "Aponte no bay" in miolo
    abertas = re.search(
        r'class="qblock"[^>]*aria-labelledby="cap2-abertas"(.*?)</section>',
        html,
        flags=re.S,
    )
    assert abertas, "subsecção perguntas abertas não encontrada"
    motor = re.search(
        r"<td>\s*Motor\s*</td>\s*<td>(.*?)</td>",
        html,
        flags=re.S,
    )
    assert motor
    bloco = (motor.group(1) + abertas.group(1)).lower()
    bloco_flat = re.sub(r"\s+", " ", bloco)
    for token in ("prefixo", "bay", "lata", "aletas", "óleo"):
        assert token in bloco_flat
    assert "térmico" in bloco_flat
    for banned in (
        "torque",
        "folga",
        "tensão",
        "tensao",
        "dínamo",
        "dinamo",
        "alternador",
        "12 v",
        "item 9",
        "multímetro",
        "multimetro",
        "fusível",
        "fusivel",
        "foto da caixa",
        "crimp",
        "ohm",
        "ω",
        "Ω",
    ):
        assert banned not in bloco_flat, banned
    assert not re.search(r"\bpn\b", bloco_flat)
    after = html[html.find("<h2>6. Checklist Aprendiz") :]
    assert "Item 9 — elétrica = N0 only" in after
    assert "tensão medida" in after.lower()
    assert "Item 9" not in abertas.group(1)
    assert "N0 only" not in abertas.group(1)
    assert html.find('id="cap2-abertas"') < html.find("Item 9 — elétrica = N0 only")
    assert html.find("Item 9 — elétrica = N0 only") < html.find('class="quiz"')


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
