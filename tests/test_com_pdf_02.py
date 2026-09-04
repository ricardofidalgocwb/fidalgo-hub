"""Guarda COM-PDF-02: proposta unpublished, só texto, sem PII/canais proibidos."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSTA = ROOT / "docs" / "propostas" / "COM-PDF-02-theodoro"
HTML = PROPOSTA / "index.html"
README = PROPOSTA / "README.md"
CSS = PROPOSTA / "print.css"


def _html() -> str:
    return HTML.read_text(encoding="utf-8")


def test_artefatos_existem():
    assert HTML.is_file()
    assert README.is_file()
    assert CSS.is_file()
    assert (PROPOSTA / "emitir-pdf.sh").is_file()


def test_nao_publicado_e_pt_br():
    html = _html()
    assert 'lang="pt-BR"' in html
    assert "noindex" in html
    assert "NÃO PUBLICADO" in html or "Não publicado" in html
    assert "não enviar ao cliente" in html.lower() or "nao enviar ao cliente" in html.lower()


def test_marca_e_pacotes_travados():
    html = _html()
    assert "Heros Custom" in html
    assert "31.402.321/0001-46" in html
    assert "(41) 99187-8091" in html
    assert "R$ 1.850" in html
    assert "R$ 4.200" in html
    assert "AIW3138" in html
    assert "Variant" in html
    assert "1975" in html
    assert "previsão de bancada" in html.lower() or "previsao de bancada" in html.lower()
    for fase in ("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"):
        assert fase in html
    assert "28" in html and "47" in html


def test_slots_ausentes_sem_img():
    html = _html()
    assert not re.search(r"<img\b", html, re.I)
    for slot in (
        "Impressão geral (print)",
        "Faróis",
        "Chicote",
        "Luz de placa",
        "Lanternas",
        "Farol E",
        "Partida",
        "Caixa de fusíveis",
    ):
        assert slot in html
    assert html.lower().count("ausente") >= 8
    assert "100 KB" in html or "100 kb" in html.lower()
    assert "especialmente" in html.lower()


def test_checklist_laudo_generico():
    html = _html().lower()
    for termo in ("oxidação", "farol e", "lanternas", "placa", "chicote", "partida"):
        assert termo.replace("ó", "o") in html.replace("ó", "o") or termo in html


def test_proibido_pii_canais_e_diagramas():
    blob = "\n".join(
        p.read_text(encoding="utf-8") for p in (HTML, CSS)
    )
    lower = blob.lower()
    assert not re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", blob)
    assert "notion.so" not in lower
    assert "notion.com" not in lower
    assert "instagram" not in lower
    assert "n8n" not in lower
    assert "type 1" not in lower
    assert "fusca" not in lower
    assert "mestra" not in lower
    assert not re.search(r"\bN0\b", blob)
    assert "cpf" not in lower


def test_readme_followup_fotos_e_refs_internas():
    readme = README.read_text(encoding="utf-8")
    assert "00_Antes" in readme
    assert "100 KB" in readme or "100 000" in readme
    assert "OS-34" in readme
    assert "PD-4" in readme
    assert "HC-2026-025" in readme
    assert "emitir-pdf" in readme
    assert "não publicado" in readme.lower() or "nao publicado" in readme.lower()
    assert "está vazia" not in readme
    assert "17 solid" in readme or "17 solid" in readme.lower()
    assert "HOLD" in readme
    assert "create_file" in readme


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
