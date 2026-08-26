"""Leitura e PATCH da Fila Founder. Escritas isoladas atrás do token + confirmação."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable
from urllib import error, request

from dotenv import load_dotenv

from dashboard.ids import fila_founder
from dashboard.status_machine import (
    ACTION_APROVAR,
    PIPELINE_STATUSES,
    Transition,
    assert_fila_founder_only_payload,
    assert_not_archived_leads,
    assert_not_os_entregue_writer,
    build_transition,
    flags_heros_vs_fse,
    n8n_allowed_for_action,
)

load_dotenv()

NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")


def notion_token() -> str | None:
    token = (os.getenv("NOTION_TOKEN") or "").strip()
    return token or None


def confirm_env() -> bool:
    return os.getenv("CONFIRM", "").strip() == "1"


def n8n_avancar_enabled() -> bool:
    flag = os.getenv("N8N_AVANCAR_ENABLED", "").strip().lower()
    return flag in {"1", "true", "yes"} and bool(os.getenv("N8N_AVANCAR_WEBHOOK", "").strip())


def writes_allowed(*, ui_confirmed: bool = False) -> bool:
    """Escreve só com token E (CONFIRM=1 ou ação UI confirmada)."""
    if not notion_token():
        return False
    return confirm_env() or bool(ui_confirmed)


@dataclass
class ActionResult:
    dry_run: bool
    written: bool
    n8n_fired: bool
    payload: dict[str, Any]
    message: str
    transition: Transition


class NotionFilaClient:
    """Cliente estreito: só consulta e PATCHa a Fila Founder."""

    def __init__(self, client: Any | None = None) -> None:
        self._cfg = fila_founder()
        self.database_id = self._cfg["database_id"]
        self._client = client

    @property
    def client(self) -> Any:
        if self._client is None:
            token = notion_token()
            if not token:
                raise RuntimeError("NOTION_TOKEN ausente — modo dry-run / sem leitura live.")
            from notion_client import Client

            self._client = Client(auth=token)
        return self._client

    def query_cards(self) -> list[dict[str, Any]]:
        assert_not_archived_leads(self.database_id)
        results: list[dict[str, Any]] = []
        start_cursor = None
        while True:
            kwargs: dict[str, Any] = {"database_id": self.database_id, "page_size": 100}
            if start_cursor:
                kwargs["start_cursor"] = start_cursor
            resp = self.client.databases.query(**kwargs)
            results.extend(resp.get("results") or [])
            if not resp.get("has_more"):
                break
            start_cursor = resp.get("next_cursor")
        return [self._normalize_page(page) for page in results]

    def apply_action(
        self,
        page_id: str,
        action: str,
        current_status: str,
        *,
        reason: str | None = None,
        ui_confirmed: bool = False,
        printer: Callable[[str], None] | None = print,
    ) -> ActionResult:
        assert_not_archived_leads(self.database_id)
        transition = build_transition(
            action,
            current_status,
            reason=reason,
            n8n_avancar_enabled=n8n_avancar_enabled(),
        )
        assert_fila_founder_only_payload(transition.properties)
        assert_not_os_entregue_writer(self.database_id, transition.properties)

        payload = {
            "page_id": page_id,
            "database_id": self.database_id,
            "properties": transition.properties,
        }
        log = transition.as_log_dict(page_id)
        text = json.dumps(log, ensure_ascii=False, indent=2)
        if printer:
            printer("=== Payload Notion (Fila Founder) ===")
            printer(text)

        dry = not writes_allowed(ui_confirmed=ui_confirmed)
        if dry:
            msg = "Dry-run: payload impresso, Notion não foi escrito."
            if not notion_token():
                msg += " Defina NOTION_TOKEN para habilitar escrita."
            elif not ui_confirmed and not confirm_env():
                msg += " Use CONFIRM=1 ou confirme na UI."
            return ActionResult(
                dry_run=True,
                written=False,
                n8n_fired=False,
                payload=payload,
                message=msg,
                transition=transition,
            )

        self.client.pages.update(page_id=page_id, properties=transition.properties)
        n8n_fired = False
        if n8n_allowed_for_action(action, n8n_avancar_enabled()):
            n8n_fired = _maybe_post_n8n(log, printer=printer)
        elif action == ACTION_APROVAR:
            if printer:
                printer("Aprovar: n8n bloqueado por contrato (Founder OK ≠ execução).")

        return ActionResult(
            dry_run=False,
            written=True,
            n8n_fired=n8n_fired,
            payload=payload,
            message="Card atualizado na Fila Founder (Notion SSOT).",
            transition=transition,
        )

    def _normalize_page(self, page: dict[str, Any]) -> dict[str, Any]:
        props = page.get("properties") or {}
        title = _title(props.get("Name"))
        status = _select(props.get("Status"))
        fila = _select(props.get("Fila"))
        recomendacao = _rich(props.get("Recomendação"))
        page_id = page.get("id") or ""
        url = page.get("url") or notion_page_url(page_id)
        return {
            "id": page_id,
            "url": url,
            "name": title,
            "status": status,
            "fila": fila,
            "nivel_l": _select(props.get("Nível L")),
            "prioridade": _select(props.get("Prioridade")),
            "handoff": _select(props.get("Handoff")),
            "confianca": _number(props.get("Confiança")),
            "gate": _multi(props.get("Gate")),
            "evento_id": _rich(props.get("evento_id")),
            "agente_origem": _select(props.get("Agente Origem")),
            "setor": _select(props.get("Setor")),
            "recomendacao": recomendacao,
            "observacoes": _rich(props.get("Observações")),
            "alerta_caixa": flags_heros_vs_fse(title, recomendacao, fila),
        }


def notion_page_url(page_id: str) -> str:
    compact = (page_id or "").replace("-", "")
    return f"https://www.notion.so/{compact}"


def empty_counts() -> dict[str, int]:
    return {status: 0 for status in PIPELINE_STATUSES}


def _select(prop: dict[str, Any] | None) -> str | None:
    if not prop:
        return None
    sel = prop.get("select")
    if not sel:
        return None
    return sel.get("name")


def _title(prop: dict[str, Any] | None) -> str:
    if not prop:
        return ""
    parts = prop.get("title") or []
    return "".join(p.get("plain_text") or p.get("text", {}).get("content") or "" for p in parts)


def _rich(prop: dict[str, Any] | None) -> str:
    if not prop:
        return ""
    parts = prop.get("rich_text") or []
    return "".join(p.get("plain_text") or p.get("text", {}).get("content") or "" for p in parts)


def _number(prop: dict[str, Any] | None) -> float | None:
    if not prop:
        return None
    return prop.get("number")


def _multi(prop: dict[str, Any] | None) -> list[str]:
    if not prop:
        return []
    return [item.get("name") for item in (prop.get("multi_select") or []) if item.get("name")]


def _maybe_post_n8n(log: dict[str, Any], printer: Callable[[str], None] | None) -> bool:
    url = os.getenv("N8N_AVANCAR_WEBHOOK", "").strip()
    if not url:
        return False
    body = json.dumps(
        {
            "source": "founder_panel",
            "brand": "Heros Custom",
            "event": "avancar",
            **log,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    key = os.getenv("N8N_WEBHOOK_KEY") or os.getenv("HEROS_WEBHOOK_KEY")
    if key:
        headers["X-Heros-Key"] = key
    req = request.Request(url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=15) as resp:
            if printer:
                printer(f"n8n webhook HTTP {resp.status}")
            return 200 <= getattr(resp, "status", 200) < 300
    except error.URLError as exc:
        if printer:
            printer(f"n8n webhook falhou (card já está Em Execução no Notion): {exc}")
        return False


def log_to_stderr(message: str) -> None:
    print(message, file=sys.stderr)
