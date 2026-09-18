"""Guarda scaffold unpublished: prompts + pipeline 3D + apparel.

HUB-tubo-3d-pesquisa-1709 · HUB-apparel-heros-1709
GitHub CI draft only · n8n Active STOP · Hotmart STOP.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
PIPELINE = ROOT / "docs" / "3d-pipeline"
BRIEFS = PIPELINE / "briefs"
APPAREL = ROOT / "apparel"
CI_DRAFT = ROOT / "docs" / "automacao" / "ci-3d-prompts-rascunho.md"

PROMPT_IDS = {
    "n0-a": ("p-n0-capa.md", "p-n0-still.md", "p-n0-check.md", "p-n0-mito.md"),
    "f-p0": ("p-fp-capa.md", "p-fp-still.md", "p-fp-flatlay.md", "p-fp-antesdepois.md"),
    "gen-f": ("p-gf-capa.md", "p-gf-hist.md", "p-gf-ponte.md"),
    "3d": ("p-3d-blockout.md", "p-3d-cutaway.md", "p-3d-explod.md", "p-3d-tex.md"),
    "ci": ("p-ci-guard.md", "p-ci-copy.md", "p-ci-slot.md"),
}

TEE_FILES = (
    "TEE-FU-01.md",
    "TEE-FU-02.md",
    "TEE-BR-01.md",
    "TEE-BR-02.md",
    "TEE-VA-01.md",
    "TEE-VA-02.md",
    "TEE-KO-01.md",
    "TEE-KO-02.md",
)

UNI_FILES = ("UNI-01.md", "UNI-02.md")

SKU_FOLDERS = ("APP-TEE", "APP-HOOD", "APP-JKT", "APP-PANT", "APP-UNI")

MOODBOARD = APPAREL / "moodboard"

MOOD_FILES = (
    ("APRL_mood_fusca_silhueta_SRC-Side_View_VW_Beetle.jpg", 615_778),
    ("APRL_mood_fuse_12v_SRC-Car_fuse_box_Layout.jpg", 382_332),
    ("APRL_mood_brasilia_SRC-VWB_Brasilia_Pocos.jpg", 621_591),
    ("APRL_mood_cultura_variante_SRC-1960s_VW_Type3_Variant.jpg", 586_823),
    ("APRL_mood_kombi_SRC-1953_VW_Kombi_T1.jpg", 762_312),
    ("APRL_mood_cultura_meme_SRC-Bugstock_14.jpg", 750_845),
    ("APRL_mood_uniforme_oficina_SRC-Dungarees_car_repair.jpg", 576_470),
    ("APRL_mood_jaqueta_servico_SRC-Bib-brace.jpg", 339_215),
    ("APRL_mood_moletom_street_SRC-VWB_1500_Fusca.jpg", 505_636),
    ("APRL_mood_fusca_T1_SRC-VWB_1500_Fusca.jpg", 505_636),
    ("APRL_mood_fusca_rua_BR_SRC-VW_Fusca_1200_1965.jpg", 742_714),
    ("APRL_mood_oficina_aircooled_bay_SRC-1962_VW_Beetle_Engine.jpg", 664_229),
    ("APRL_mood_oficina_classic_SRC-VW_Kaferproduktion.jpg", 739_814),
)

TEE_MOCKS = (
    "mock-TEE-FU-01.html",
    "mock-TEE-FU-02.html",
    "mock-TEE-BR-01.html",
    "mock-TEE-BR-02.html",
    "mock-TEE-VA-01.html",
    "mock-TEE-VA-02.html",
    "mock-TEE-KO-01.html",
    "mock-TEE-KO-02.html",
)

UNI_MOCKS = ("mock-UNI-01.html", "mock-UNI-02.html")

BINARY_3D = {".glb", ".gltf", ".fbx", ".obj", ".blend", ".stl"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_prompts_tree_and_readme_headers():
    readme = _read(PROMPTS / "README.md")
    for token in (
        "N0-A",
        "F-P0",
        "C2",
        "GEN-F",
        "HA-E",
        "3D",
        "CI",
        "Hotmart STOP",
        "COM → VIS → ENT",
        "5 eixos",
        "Estilo base",
        "Negativo",
        "Oliver",
        "#C9A227",
        "n8n Active STOP",
    ):
        assert token in readme, token
    assert "docs/3d-pipeline/README.md" in readme


def test_prompt_ids_exist():
    for folder, names in PROMPT_IDS.items():
        for name in names:
            path = PROMPTS / folder / name
            assert path.is_file(), path
            text = _read(path)
            pid = {
                "p-n0-capa.md": "P-N0-capa",
                "p-n0-still.md": "P-N0-still",
                "p-n0-check.md": "P-N0-check",
                "p-n0-mito.md": "P-N0-mito",
                "p-fp-capa.md": "P-FP-capa",
                "p-fp-still.md": "P-FP-still",
                "p-fp-flatlay.md": "P-FP-flatlay",
                "p-fp-antesdepois.md": "P-FP-antesdepois",
                "p-gf-capa.md": "P-GF-capa",
                "p-gf-hist.md": "P-GF-hist",
                "p-gf-ponte.md": "P-GF-ponte",
                "p-3d-blockout.md": "P-3D-blockout",
                "p-3d-cutaway.md": "P-3D-cutaway",
                "p-3d-explod.md": "P-3D-explod",
                "p-3d-tex.md": "P-3D-tex",
                "p-ci-guard.md": "P-CI-guard",
                "p-ci-copy.md": "P-CI-copy",
                "p-ci-slot.md": "P-CI-slot",
            }[name]
            assert pid in text, (path, pid)
            assert "Hotmart STOP" in text or "n8n Active STOP" in text
    assert (PROMPTS / "n0-a" / "roteiro-a1-a6.md").is_file()
    assert (PROMPTS / "f-p0" / "roteiro-cap2-passaporte.md").is_file()
    roteiro = _read(PROMPTS / "n0-a" / "roteiro-a1-a6.md")
    assert "objetivo → por quê → como → cheque → erro → próximo" in roteiro
    assert "Oliver" in roteiro
    assert "sem vídeo embed" in roteiro


def test_3d_pipeline_tree_and_briefs():
    readme = _read(PIPELINE / "README.md")
    for token in (
        "Pesquisa/VIS",
        "≥100KB",
        "TEC PASS|HOLD",
        "ACE slot",
        "ENT unpublished",
        "APR",
        "brief",
        "modelo",
        "textura",
        "T1 ≠ T3",
        "3D-CH|MO|EL-P0",
        "Hotmart STOP",
        "Oliver",
    ):
        assert token in readme, token
    assert "prompts/3d" in readme or "prompts/3d/" in readme

    mapping = {
        "fusca-p0-chassi.md": ("3D-CH-P0", "3df7d36bae64811db8ebd95f02dbb21a"),
        "fusca-p0-motor.md": ("3D-MO-P0", "3df7d36bae64811db8ebd95f02dbb21a"),
        "fusca-p0-eletrico.md": ("3D-EL-P0", "3df7d36bae648163a85ec037aa7543cd"),
    }
    for name, (slot, notion) in mapping.items():
        path = BRIEFS / name
        text = _read(path)
        assert slot in text, (name, slot)
        assert notion in text, name
        assert "Hotmart STOP" in text
        assert "Oliver" in text
        assert "TODO" in text
        assert "3D-" in text and "P0" in text

    eletrico = _read(BRIEFS / "fusca-p0-eletrico.md")
    assert "caixa" in eletrico.lower()
    assert "CS-1" in eletrico
    assert "bandeja" in eletrico.lower()
    assert "letterform" in eletrico.lower()
    assert "GAP" in eletrico

    for folder in ("3d-ch-p0", "3d-mo-p0", "3d-el-p0"):
        keep = PIPELINE / "assets" / folder / ".gitkeep"
        assert keep.is_file(), keep


def test_no_binary_3d_assets():
    for path in PIPELINE.rglob("*"):
        if path.is_file() and path.suffix.lower() in BINARY_3D:
            raise AssertionError(f"binário 3D não permitido neste rascunho: {path}")
        if path.is_file() and path.stat().st_size >= 100_000 and path.suffix.lower() not in {".md", ""}:
            raise AssertionError(f"ficheiro grande fora de markdown: {path}")


def test_ci_rascunho_n8n_stop():
    text = _read(CI_DRAFT)
    assert "n8n Active" in text
    assert "STOP" in text
    assert "GitHub CI" in text
    assert "test_prompts_3d_scaffold.py" in text
    assert "Hotmart STOP" in text


def test_apparel_skus_and_bible():
    readme = _read(APPAREL / "README.md")
    for token in (
        "APP-TEE",
        "APP-HOOD",
        "APP-JKT",
        "APP-PANT",
        "APP-UNI",
        "#C9A227",
        "#0D0D0D",
        "#F5F0E6",
        "Hotmart STOP",
        "n8n Active STOP",
        "3df7d36bae6481f69fa2d278b67b4507",
        "VEN GTM",
        "Founder OK",
        "Variante",
        "≠ Mestra",
        "1YOk5ImGO1mwQB-qPpjQQclQ_zgWPjIGg",
        "moodboard",
    ):
        assert token in readme, token
    assert "439" in readme
    assert "557" in readme

    for sku in SKU_FOLDERS:
        folder = APPAREL / sku
        assert folder.is_dir(), sku
        assert (folder / "README.md").is_file(), sku

    hood = _read(APPAREL / "APP-HOOD" / "README.md")
    jkt = _read(APPAREL / "APP-JKT" / "README.md")
    pant = _read(APPAREL / "APP-PANT" / "README.md")
    assert "artes P1" in hood
    assert "artes P1" in jkt
    assert "artes P1" in pant


def test_apparel_eight_tee_two_uni():
    for name in TEE_FILES:
        path = APPAREL / "APP-TEE" / name
        assert path.is_file(), name
        text = _read(path)
        assert name.replace(".md", "") in text
        assert "Hotmart STOP" in text
        assert "TODO mockup VIS" in text
    for name in UNI_FILES:
        path = APPAREL / "APP-UNI" / name
        assert path.is_file(), name
        text = _read(path)
        assert name.replace(".md", "") in text
        assert "Hotmart STOP" in text

    fu01 = _read(APPAREL / "APP-TEE" / "TEE-FU-01.md")
    assert "FUSCA A AR" in fu01
    assert "TYPE 1" in fu01
    assert "rodou gerações" in fu01

    fu02 = _read(APPAREL / "APP-TEE" / "TEE-FU-02.md")
    assert "1968" in fu02
    assert "12 V ≠ CHUTE" in fu02
    assert "Meça parado." in fu02
    assert "frente+verso" in fu02

    br01 = _read(APPAREL / "APP-TEE" / "TEE-BR-01.md")
    assert "BRASÍLIA" in br01
    br02 = _read(APPAREL / "APP-TEE" / "TEE-BR-02.md")
    assert "reta e critério" in br02

    va01 = _read(APPAREL / "APP-TEE" / "TEE-VA-01.md")
    assert "≠ Mestra" in va01
    va02 = _read(APPAREL / "APP-TEE" / "TEE-VA-02.md")
    assert "outra linha, mesmo ar" in va02

    ko01 = _read(APPAREL / "APP-TEE" / "TEE-KO-01.md")
    assert "KOMBI" in ko01
    ko02 = _read(APPAREL / "APP-TEE" / "TEE-KO-02.md")
    assert "LOTADA DE HISTÓRIA" in ko02
    assert "Tipografia" in ko02

    uni01 = _read(APPAREL / "APP-UNI" / "UNI-01.md")
    assert "HEROS CUSTOM" in uni01
    assert "AIR-COOLED" in uni01
    assert "SERVIÇO · EVIDÊNCIA" in uni01
    assert "QR" in uni01

    uni02 = _read(APPAREL / "APP-UNI" / "UNI-02.md")
    assert "HC" in uni02
    assert "primeiro nome" in uni02
    assert "40–60 mm" in uni02 or "40-60 mm" in uni02


def test_apparel_moodboard_exact_bytes():
    assert (MOODBOARD / "INDEX-TEE-UNI.md").is_file()
    assert (MOODBOARD / "MANIFEST.txt").is_file()
    assert len(MOOD_FILES) == 13
    for name, expected in MOOD_FILES:
        path = MOODBOARD / name
        assert path.is_file(), name
        size = path.stat().st_size
        assert size == expected, (name, size, expected)
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", name


def test_apparel_mock_html_unpublished():
    pages = [APPAREL / "APP-TEE" / name for name in TEE_MOCKS]
    pages += [APPAREL / "APP-UNI" / name for name in UNI_MOCKS]
    assert len(pages) == 10
    banned = ("R$", "hotmart", "checkout", "n8n Active")
    for path in pages:
        assert path.is_file(), path
        html = _read(path)
        assert "UNPUBLISHED" in html
        assert "#c9a227" in html.lower() or "mock.css" in html
        assert "Drive cite" in html
        for token in banned:
            assert token.lower() not in html.lower(), (path, token)
        stem = path.name.replace("mock-", "").replace(".html", "")
        stub = path.with_name(f"{stem}.md")
        assert stub.is_file(), stub
        assert path.name in _read(stub)


def test_scaffold_sem_preco_nem_checkout():
    banned = ("R$", "hotmart.com", "n8n Active = 1", "N8N_AVANCAR_ENABLED=1")
    roots = (PROMPTS, PIPELINE, APPAREL, CI_DRAFT.parent)
    for root in roots:
        paths = [root] if root.is_file() else list(root.rglob("*.md"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for token in banned:
                assert token not in text, (path, token)
