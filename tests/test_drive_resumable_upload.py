"""Portão de tamanho do upload Drive — sem API live, sem n8n."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.drive_resumable_upload import (
    MIN_EVIDENCE_BYTES,
    DriveUploadError,
    assert_local_size,
    assert_secret_outside_repo,
    build_plan,
    main,
    remote_size_ok,
    upload_and_verify,
)


def test_limiar_e_100kb_decimal():
    assert MIN_EVIDENCE_BYTES == 100_000


def test_recusa_ficheiro_menor_ou_igual_a_100kb(tmp_path: Path):
    stub = tmp_path / "mcp_stub.jpg"
    stub.write_bytes(b"\xff\xd8" + b"x" * 8_000)  # ~8 KB — típico do MCP
    with pytest.raises(DriveUploadError, match="Recusado"):
        assert_local_size(stub)
    exact = tmp_path / "exact.bin"
    exact.write_bytes(b"a" * MIN_EVIDENCE_BYTES)
    with pytest.raises(DriveUploadError, match="Recusado"):
        assert_local_size(exact)


def test_aceita_ficheiro_acima_de_100kb(tmp_path: Path):
    ok = tmp_path / "antes.jpg"
    ok.write_bytes(b"a" * (MIN_EVIDENCE_BYTES + 1))
    assert assert_local_size(ok) == MIN_EVIDENCE_BYTES + 1


def test_recusa_ficheiro_inexistente(tmp_path: Path):
    missing = tmp_path / "nao_existe.jpg"
    with pytest.raises(DriveUploadError, match="inexistente"):
        assert_local_size(missing)


def test_cli_dry_run_recusa_stub_sem_chamar_drive(tmp_path: Path, capsys):
    stub = tmp_path / "stub.jpg"
    stub.write_bytes(b"stub" * 200)
    rc = main(
        [
            "--parent",
            "1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-",
            "--file",
            str(stub),
            "--dry-run",
        ]
    )
    assert rc == 2
    out = capsys.readouterr().out
    assert "dry_run" in out
    assert "would_upload" in out
    assert "false" in out.lower()
    assert "n8n" in out


def test_cli_dry_run_plano_ok_sem_upload(tmp_path: Path, capsys):
    photo = tmp_path / "antes.jpg"
    photo.write_bytes(b"P" * (MIN_EVIDENCE_BYTES + 50))
    rc = main(
        [
            "--parent",
            "1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-",
            "--file",
            str(photo),
            "--name",
            "OS-34_Antes_caixa_fusiveis.jpg",
            "--dry-run",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "OS-34_Antes_caixa_fusiveis.jpg" in out
    assert "resumable" in out
    assert '"written": false' in out
    plan = build_plan("parent-id", photo, "foto.jpg")
    assert plan["would_upload"] is True
    assert plan["local_size"] == MIN_EVIDENCE_BYTES + 50


def test_recusa_credencial_dentro_do_clone():
    inside = Path(__file__).resolve().parents[1] / "would-be-secret.json"
    with pytest.raises(DriveUploadError, match="dentro do clone"):
        assert_secret_outside_repo(inside)


def test_remote_size_recusa_stub_sem_api():
    with pytest.raises(DriveUploadError, match="size"):
        remote_size_ok({"id": "abc", "size": "4096"})
    with pytest.raises(DriveUploadError, match="sem campo size"):
        remote_size_ok({"id": "abc"})
    assert remote_size_ok({"size": "100001"}) == 100_001


def test_upload_and_verify_lixeira_se_remoto_for_stub(tmp_path: Path):
    """Portão remoto sem libs Google e sem HTTP."""
    photo = tmp_path / "antes.jpg"
    photo.write_bytes(b"P" * (MIN_EVIDENCE_BYTES + 1))
    trashed: list[str] = []

    def fake_upload(_svc, _parent, _path, _name):
        return {"id": "file-stub", "name": "x.jpg"}

    def fake_meta(_svc, file_id):
        return {"id": file_id, "name": "x.jpg", "size": "8192"}

    def fake_trash(_svc, file_id):
        trashed.append(file_id)

    with pytest.raises(DriveUploadError, match="lixeira"):
        upload_and_verify(
            "parent-id",
            photo,
            uploader=fake_upload,
            metadata_fetcher=fake_meta,
            trasher=fake_trash,
        )
    assert trashed == ["file-stub"]
