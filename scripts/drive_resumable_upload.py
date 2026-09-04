#!/usr/bin/env python3
"""Upload resumable para o Google Drive — evidência fotográfica.

Proibido: MCP Drive create_file / base64 (gera stub de 3–9 KB).
Aceite: ficheiro local e remoto com size > 100 000 bytes.

Auth (nunca no git): ver scripts/README.md
  GOOGLE_APPLICATION_CREDENTIALS          service account JSON
  GOOGLE_DRIVE_OAUTH_CLIENT_SECRETS       OAuth client secret JSON
  GOOGLE_DRIVE_OAUTH_TOKEN                token gravado fora do repo

SSOT: docs/drive-binary-upload.md
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any

# 100 KB decimal — o mesmo limiar do SSOT e do teste.
MIN_EVIDENCE_BYTES = 100_000

OS34_ANTES_FOLDER_ID = "1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-"
DRIVE_SCOPE = "https://www.googleapis.com/auth/drive.file"

# Chunk resumable tem de ser múltiplo de 256 KiB.
RESUMABLE_CHUNK_BYTES = 256 * 1024


class DriveUploadError(Exception):
    """Falha local (portão) ou remota (metadado / API)."""


def assert_local_size(path: Path, min_bytes: int = MIN_EVIDENCE_BYTES) -> int:
    """Recusa ficheiro inexistente ou com size ≤ min_bytes. Não chama Drive."""
    if not path.is_file():
        raise DriveUploadError(f"Recusado: ficheiro inexistente: {path}")
    size = path.stat().st_size
    if size <= min_bytes:
        raise DriveUploadError(
            f"Recusado: {path} tem {size} bytes (≤ {min_bytes}). "
            "MCP create_file/base64 gera stubs de 3–9 KB. "
            "Use original de câmara > 100 KB (docs/drive-binary-upload.md)."
        )
    return size


def remote_size_ok(metadata: dict[str, Any], min_bytes: int = MIN_EVIDENCE_BYTES) -> int:
    """Lê metadata['size'] e exige > min_bytes. Sem rede."""
    raw = metadata.get("size")
    if raw is None or raw == "":
        raise DriveUploadError(
            "Falha: metadado Drive sem campo size. Não aceitar como evidência."
        )
    try:
        size = int(raw)
    except (TypeError, ValueError) as exc:
        raise DriveUploadError(f"Falha: size Drive inválido: {raw!r}") from exc
    if size <= min_bytes:
        raise DriveUploadError(
            f"Falha: Drive size={size} bytes (≤ {min_bytes}). "
            "Stub ou truncado — mover para lixeira e repetir Path A/B."
        )
    return size


def build_plan(
    parent: str,
    path: Path,
    name: str | None = None,
    *,
    min_bytes: int = MIN_EVIDENCE_BYTES,
) -> dict[str, Any]:
    """Plano de dry-run. Avalia o portão local; não chama a API."""
    display_name = name or path.name
    plan: dict[str, Any] = {
        "dry_run": True,
        "written": False,
        "n8n": False,
        "parent": parent,
        "file": str(path),
        "name": display_name,
        "min_bytes": min_bytes,
        "upload_type": "resumable",
        "mcp_create_file": False,
    }
    try:
        size = assert_local_size(path, min_bytes=min_bytes)
    except DriveUploadError as exc:
        plan["ok"] = False
        plan["would_upload"] = False
        plan["local_size"] = path.stat().st_size if path.is_file() else None
        plan["error"] = str(exc)
        return plan
    plan["ok"] = True
    plan["would_upload"] = True
    plan["local_size"] = size
    plan["message"] = (
        f"Plano: resumable upload de {display_name} ({size} bytes) → pasta {parent}. "
        "Sem MCP. Sem n8n."
    )
    return plan


def _google_modules() -> dict[str, Any]:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import service_account
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise DriveUploadError(
            "Path B exige libs Google (não estão no requirements.txt do painel): "
            "pip install google-api-python-client google-auth "
            "google-auth-oauthlib google-auth-httplib2. "
            "Sem auth no git. Ver scripts/README.md."
        ) from exc
    return {
        "Request": Request,
        "service_account": service_account,
        "Credentials": Credentials,
        "InstalledAppFlow": InstalledAppFlow,
        "build": build,
        "MediaFileUpload": MediaFileUpload,
    }


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def assert_secret_outside_repo(path: Path) -> Path:
    """Recusa JSON de credencial/token dentro do clone — nunca no git."""
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(_repo_root())
    except ValueError:
        return resolved
    raise DriveUploadError(
        f"Recusado: credencial/token dentro do clone ({resolved}). "
        "Use um caminho fora do repo (ex.: ~/.config/fidalgo-hub/). "
        "Não commitar secrets."
    )


def load_credentials() -> Any:
    """Service account (GOOGLE_APPLICATION_CREDENTIALS) ou OAuth local."""
    g = _google_modules()
    sa_path = (os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or "").strip()
    if sa_path:
        path = assert_secret_outside_repo(Path(sa_path))
        if not path.is_file():
            raise DriveUploadError(
                f"GOOGLE_APPLICATION_CREDENTIALS não é um ficheiro: {path}"
            )
        return g["service_account"].Credentials.from_service_account_file(
            str(path), scopes=[DRIVE_SCOPE]
        )

    client_path = (os.environ.get("GOOGLE_DRIVE_OAUTH_CLIENT_SECRETS") or "").strip()
    token_path_raw = (os.environ.get("GOOGLE_DRIVE_OAUTH_TOKEN") or "").strip()
    if client_path:
        client = assert_secret_outside_repo(Path(client_path))
        if not client.is_file():
            raise DriveUploadError(
                f"GOOGLE_DRIVE_OAUTH_CLIENT_SECRETS não é um ficheiro: {client}"
            )
        token_path = assert_secret_outside_repo(
            Path(token_path_raw)
            if token_path_raw
            else Path.home() / ".config" / "fidalgo-hub" / "drive_token.json"
        )
        creds = None
        if token_path.is_file():
            creds = g["Credentials"].from_authorized_user_file(
                str(token_path), [DRIVE_SCOPE]
            )
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(g["Request"]())
        if not creds or not creds.valid:
            flow = g["InstalledAppFlow"].from_client_secrets_file(
                str(client), [DRIVE_SCOPE]
            )
            creds = flow.run_local_server(port=0)
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_text(creds.to_json(), encoding="utf-8")
        return creds

    raise DriveUploadError(
        "Sem credencial Drive. Defina GOOGLE_APPLICATION_CREDENTIALS "
        "ou GOOGLE_DRIVE_OAUTH_CLIENT_SECRETS (+ GOOGLE_DRIVE_OAUTH_TOKEN). "
        "Não commitar JSON. Path A = drop manual no browser. "
        "Ver scripts/README.md."
    )


def _drive_service(creds: Any) -> Any:
    g = _google_modules()
    return g["build"]("drive", "v3", credentials=creds, cache_discovery=False)


def _guess_mime(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


def trash_file(service: Any, file_id: str) -> None:
    service.files().update(
        fileId=file_id,
        body={"trashed": True},
        supportsAllDrives=True,
    ).execute()


def fetch_metadata(service: Any, file_id: str) -> dict[str, Any]:
    return (
        service.files()
        .get(
            fileId=file_id,
            fields="id,name,size,mimeType,md5Checksum,parents",
            supportsAllDrives=True,
        )
        .execute()
    )


def resumable_upload(
    service: Any,
    parent: str,
    path: Path,
    name: str,
) -> dict[str, Any]:
    """MediaFileUpload resumable — não é multipart/base64 de uma vez."""
    g = _google_modules()
    media = g["MediaFileUpload"](
        str(path),
        mimetype=_guess_mime(path),
        resumable=True,
        chunksize=RESUMABLE_CHUNK_BYTES,
    )
    if not getattr(media, "resumable", False):
        raise DriveUploadError("MediaFileUpload não está em modo resumable.")
    request = service.files().create(
        body={"name": name, "parents": [parent]},
        media_body=media,
        fields="id,name,size,mimeType,md5Checksum,parents",
        supportsAllDrives=True,
    )
    response: dict[str, Any] | None = None
    while response is None:
        _status, response = request.next_chunk()
    if not response or not response.get("id"):
        raise DriveUploadError("Upload resumable sem id de ficheiro.")
    return response


def upload_and_verify(
    parent: str,
    path: Path,
    name: str | None = None,
    *,
    min_bytes: int = MIN_EVIDENCE_BYTES,
    service: Any | None = None,
    uploader: Any | None = None,
    metadata_fetcher: Any | None = None,
    trasher: Any | None = None,
) -> dict[str, Any]:
    """Portão local → upload resumable → files.get → trash se size falhar.

    Hooks (`uploader` / `metadata_fetcher` / `trasher`) existem para teste
    sem libs Google e sem API live.
    """
    local_size = assert_local_size(path, min_bytes=min_bytes)
    display_name = name or path.name
    svc = service
    if svc is None and uploader is None:
        svc = _drive_service(load_credentials())
    created = (uploader or resumable_upload)(svc, parent, path, display_name)
    file_id = created["id"]
    fetch = metadata_fetcher or fetch_metadata
    do_trash = trasher or trash_file
    try:
        meta = fetch(svc, file_id)
        remote_size = remote_size_ok(meta, min_bytes=min_bytes)
    except DriveUploadError as exc:
        try:
            do_trash(svc, file_id)
        except Exception as trash_exc:  # noqa: BLE001 — reportar os dois
            raise DriveUploadError(
                f"size inválido após upload (id={file_id}); "
                f"lixeira também falhou: {trash_exc}"
            ) from trash_exc
        raise DriveUploadError(
            f"Upload id={file_id} foi para a lixeira: {exc}"
        ) from exc
    return {
        "ok": True,
        "dry_run": False,
        "written": True,
        "n8n": False,
        "id": file_id,
        "name": meta.get("name") or display_name,
        "parent": parent,
        "local_size": local_size,
        "size": remote_size,
        "mimeType": meta.get("mimeType"),
        "md5Checksum": meta.get("md5Checksum"),
        "upload_type": "resumable",
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upload resumable Drive com portão > 100 KB. "
            "Proibido MCP create_file. Sem n8n."
        )
    )
    parser.add_argument(
        "--parent",
        required=True,
        help=f"ID da pasta Drive (OS-34 00_Antes = {OS34_ANTES_FOLDER_ID})",
    )
    parser.add_argument("--file", required=True, help="Caminho local do ficheiro")
    parser.add_argument(
        "--name",
        default=None,
        help="Nome no Drive (padrão: basename de --file)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Só imprime o plano. Não chama Drive.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    path = Path(args.file).expanduser()
    if args.dry_run:
        plan = build_plan(args.parent, path, args.name)
        print("=== Drive upload — dry-run (sem API, sem n8n, sem MCP) ===")
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0 if plan.get("ok") else 2
    try:
        result = upload_and_verify(args.parent, path, args.name)
    except DriveUploadError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
