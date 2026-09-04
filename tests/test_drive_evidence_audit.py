"""Portão stub/solid e tipagem — sem Drive live, sem Notion write, sem n8n."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dashboard.ids import (
    CLIENTES_ID,
    COMECE_AQUI_PAGE_ID,
    CRM_OPORTUNIDADES_ID,
    OS_DATABASE_ID,
    PASSAPORTE_CABECA_DATA_SOURCE_ID,
    PASSAPORTE_CABECA_ID,
    PASSAPORTE_LINHAS_DATA_SOURCE_ID,
    PASSAPORTE_LINHAS_ID,
    load_drive_ids,
    load_ids,
)
from scripts.drive_evidence_audit import (
    DriveAuditError,
    audit_manifest,
    classify_item,
    classify_size,
    filename_matches_slot,
    load_manifest,
    main,
    parse_manifest,
    slot_tokens,
    tipagem_catalog,
    tipagem_coverage,
)
from scripts.drive_resumable_upload import MIN_EVIDENCE_BYTES


def test_limiar_igual_ao_upload():
    assert MIN_EVIDENCE_BYTES == 100_000
    assert classify_size(100_000) == "stub"
    assert classify_size(100_001) == "solid"
    assert classify_size(0) == "stub"
    assert classify_size(8_192) == "stub"


def test_classify_item_pasta_sem_size():
    row = classify_item(
        {
            "name": "00_Cliente_envia",
            "id": "1dgBWAfYnqsAOrUPFulUAPZJxKf1n_ASl",
            "mimeType": "application/vnd.google-apps.folder",
        }
    )
    assert row["class"] == "skip"
    assert row["kind"] == "folder"


def test_classify_item_size_invalido():
    row = classify_item({"name": "x.jpg", "id": "abc", "size": "não-número"})
    assert row["class"] == "invalid"


def test_slot_tokens_chicote_e_prefixo():
    tokens = slot_tokens("03_chicote/lanterna")
    assert "03_chicote" in tokens
    assert "chicote" in tokens
    assert "lanterna" in tokens
    assert slot_tokens("00_print_zap")[0] == "00_print_zap"
    assert "print_zap" in slot_tokens("00_print_zap")


def test_caixa_audit_preenche_caixa_e_print_zap():
    name = "AIW3138_00_Antes_10_caixa_fusiveis_print_zap.png"
    assert filename_matches_slot(name, "10_caixa_fusiveis")
    assert filename_matches_slot(name, "00_print_zap")
    assert not filename_matches_slot(name, "02_farol_E")
    assert not filename_matches_slot("00_Antes_vazio.txt", "00_print_zap")


def test_tipagem_gaps_vs_catalogo():
    catalog = tipagem_catalog(load_drive_ids())
    assert catalog == [
        "02_farol_E",
        "03_chicote/lanterna",
        "04_luz_placa",
        "07_partida",
        "10_caixa_fusiveis",
        "00_print_zap",
    ]
    cov = tipagem_coverage(
        ["AIW3138_00_Antes_10_caixa_fusiveis_print_zap.png"],
        catalog,
    )
    assert "10_caixa_fusiveis" in cov["present"]
    assert "00_print_zap" in cov["present"]
    assert "02_farol_E" in cov["gaps"]
    assert "07_partida" in cov["gaps"]


def test_audit_stubs_falham_gaps_nao(tmp_path: Path):
    items = [
        {"name": "mcp_stub.jpg", "size": 4096, "id": "stub-1"},
        {
            "name": "AIW3138_02_farol_E.jpg",
            "size": 150_000,
            "id": "solid-1",
        },
    ]
    report = audit_manifest(items)
    assert report["dry_run"] is True
    assert report["written"] is False
    assert report["n8n"] is False
    assert report["live_drive"] is False
    assert report["ok"] is False
    assert report["counts"]["stub"] == 1
    assert report["counts"]["solid"] == 1
    assert "07_partida" in report["tipagem"]["gaps"]


def test_audit_so_solid_ok_mesmo_com_gap():
    items = [
        {
            "name": "AIW3138_00_Antes_10_caixa_fusiveis_print_zap.png",
            "size": "2842327",
            "id": "1qO4OS7GdJAfmxUrvH0PbosEgGKjvtICC",
        }
    ]
    report = audit_manifest(items)
    assert report["ok"] is True
    assert report["counts"]["stub"] == 0
    assert report["counts"]["solid"] == 1
    assert report["tipagem"]["gaps"]  # catálogo ainda tem lacunas
    assert "10_caixa_fusiveis" in report["tipagem"]["present"]


def test_cli_manifest_stub_exit_nonzero(tmp_path: Path, capsys):
    manifest = tmp_path / "files.json"
    manifest.write_text(
        json.dumps(
            [
                {"name": "stub.png", "size": 100_000, "id": "eq"},
            ]
        ),
        encoding="utf-8",
    )
    rc = main(["--manifest", str(manifest)])
    assert rc == 2
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["ok"] is False
    assert payload["counts"]["stub"] == 1
    assert payload["dry_run"] is True


def test_cli_manifest_solid_exit_zero(tmp_path: Path, capsys):
    manifest = tmp_path / "files.json"
    manifest.write_text(
        json.dumps(
            {
                "files": [
                    {
                        "name": "AIW3138_07_partida.jpg",
                        "size": 100_001,
                        "id": "ok-1",
                    },
                    {
                        "name": "00_Cliente_envia",
                        "id": "folder",
                        "mimeType": "application/vnd.google-apps.folder",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    rc = main(["--manifest", str(manifest)])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["counts"]["solid"] == 1
    assert payload["counts"]["folders_skipped"] == 1
    assert "07_partida" in payload["tipagem"]["present"]


def test_cli_manifest_ausente(tmp_path: Path):
    rc = main(["--manifest", str(tmp_path / "nao.json")])
    assert rc == 2


def test_parse_manifest_rejeita_formato_errado():
    with pytest.raises(DriveAuditError):
        parse_manifest({"oops": []})
    with pytest.raises(DriveAuditError):
        parse_manifest("x")
    assert load_drive_ids()["os34"]["folders"]["00_Antes"] == (
        "1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-"
    )


def test_load_manifest_json_invalido(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(DriveAuditError, match="inválido"):
        load_manifest(bad)


def test_drive_ids_os34_e_caixa():
    cfg = load_drive_ids()
    assert cfg["fetched_at"] == "2026-09-04"
    assert cfg["min_evidence_bytes"] == 100_000
    os34 = cfg["os34"]
    assert os34["root_id"] == "1wJSiE_gmqMnLUkt18lB75YCpxzMxz_Oy"
    assert os34["folders"]["02_Fotos"] == "1IWdCBE5NPbOpZexm2mGNA2t9XohHUo7f"
    assert os34["folders"]["00_Cliente_envia"] == "1dgBWAfYnqsAOrUPFulUAPZJxKf1n_ASl"
    caixa = os34["evidence"]["caixa_fusiveis"]
    assert caixa["id"] == "1qO4OS7GdJAfmxUrvH0PbosEgGKjvtICC"
    assert caixa["size"] == 2_842_327
    assert "twin" in os34["notes"]
    blob = json.dumps(cfg).lower()
    assert "private_key" not in blob
    assert "client_secret" not in blob
    assert "não são secrets" in cfg["comment"].lower()


def test_notion_ids_write_false_e_twin():
    cfg = load_ids()
    assert cfg["fetched_at"] == "2026-09-04"
    dbs = cfg["databases"]
    for key in (
        "os",
        "crm_oportunidades",
        "clientes",
        "passaporte_cabeca",
        "passaporte_linhas",
        "fila_editorial",
    ):
        assert dbs[key]["write"] is False, key
    assert dbs["fila_editorial"]["runner_only"] is True
    assert dbs["os"]["data_source_id"] == "2987d36b-ae64-824f-a9e1-87f5ba4e7a7c"
    assert dbs["crm_oportunidades"]["data_source_id"] == (
        "7577d36b-ae64-835e-9e3d-0788304619bc"
    )
    assert dbs["clientes"]["data_source_id"] == (
        "3067d36b-ae64-82d6-ae7f-07290c4bac94"
    )
    assert dbs["os"]["database_id"] == OS_DATABASE_ID
    assert dbs["crm_oportunidades"]["database_id"] == CRM_OPORTUNIDADES_ID
    assert dbs["clientes"]["database_id"] == CLIENTES_ID
    assert dbs["passaporte_cabeca"]["database_id"] == PASSAPORTE_CABECA_ID
    assert dbs["passaporte_cabeca"]["data_source_id"] == (
        PASSAPORTE_CABECA_DATA_SOURCE_ID
    )
    assert dbs["passaporte_linhas"]["database_id"] == PASSAPORTE_LINHAS_ID
    assert dbs["passaporte_linhas"]["data_source_id"] == (
        PASSAPORTE_LINHAS_DATA_SOURCE_ID
    )
    assert cfg["pages"]["comece_aqui"]["id"] == COMECE_AQUI_PAGE_ID
    twin = cfg["twins"]["aiw3138"]
    assert twin["ice_head"]["codigo"] == "HC-2026-025"
    assert twin["comercial"]["codigo"] == "OS-34"
    assert twin["shared_drive_root_id"] == "1wJSiE_gmqMnLUkt18lB75YCpxzMxz_Oy"
    assert dbs["fila_founder"]["write"] is True
