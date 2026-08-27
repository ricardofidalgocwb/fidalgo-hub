"""Leitura e PATCH da Fila Editorial. Escritas só com token + CONFIRM=1.

Sem Instagram, sem site, sem n8n, sem webhook. Aprovar nunca publica.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable

from dotenv import load_dotenv

from editorial.canon import scan_card
from editorial.ids import assert_editorial_database, fila_editorial
from editorial.status_machine import (
    ACTION_NOVO,
    PIPELINE_STATUSES,
    Transition,
    assert_canal_nao_publicar_on_create,
    assert_editorial_only_payload,
    assert_never_automacao_true,
    assert_never_publicado,
    build_transition,
    publish_allowed_for_action,
)

load_dotenv()

NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")


def notion_token() -> str | None:
    token = (os.getenv("NOTION_TOKEN") or "").strip()
    return token or None


def confirm_env() -> bool:
    return os.getenv("CONFIRM", "").strip() == "1"


def writes_allowed() -> bool:
    """Escreve só com NOTION_TOKEN e CONFIRM=1. Sem atalho de UI."""
    return bool(notion_token()) and confirm_env()


@dataclass
class ActionResult:
    dry_run: bool
    written: bool
    published: bool
    n8n_fired: bool
    instagram_posted: bool
    payload: dict[str, Any]
    message: str
    transition: Transition


class NotionEditorialClient:
    """Cliente estreito: só consulta e PATCHa a Fila Editorial."""

    def __init__(self, client: Any | None = None) -> None:
        self._cfg = fila_editorial()
        self.database_id = self._cfg["database_id"]
        self._client = client

    @property
    def client(self) -> Any:
        if self._client is None:
            token = notion_token()
            if not token:
                raise RuntimeError(
                    "NOTION_TOKEN ausente — modo dry-run / sem leitura live."
                )
            from notion_client import Client

            self._client = Client(auth=token)
        return self._client

    def query_cards(self) -> list[dict[str, Any]]:
        assert_editorial_database(self.database_id)
        results: list[dict[str, Any]] = []
        start_cursor = None
        while True:
            kwargs: dict[str, Any] = {
                "database_id": self.database_id,
                "page_size": 100,
            }
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
        action: str,
        *,
        page_id: str | None = None,
        current_status: str | None = None,
        reason: str | None = None,
        peca: str | None = None,
        metrica: str | None = None,
        observacoes: str | None = None,
        proxima_acao: str | None = None,
        braco: str | None = None,
        porta: str | None = None,
        formato: str | None = None,
        printer: Callable[[str], None] | None = print,
    ) -> ActionResult:
        assert_editorial_database(self.database_id)
        creating = action == ACTION_NOVO
        if not creating and not page_id:
            raise RuntimeError("page_id é obrigatório para Aprovar/Recusar/Adiar.")

        card_fields = {
            "peca": peca,
            "metrica": metrica,
            "observacoes": observacoes,
            "proxima_acao": proxima_acao,
        }
        transition = build_transition(
            action,
            current_status,
            reason=reason,
            braco=braco,
            porta=porta,
            formato=formato,
            **card_fields,
        )
        assert_editorial_only_payload(transition.properties, creating=creating)
        assert_never_publicado(transition.properties)
        assert_never_automacao_true(transition.properties)
        if creating:
            assert_canal_nao_publicar_on_create(transition.properties)

        if publish_allowed_for_action(action):
            raise RuntimeError("Contrato violado: publish_allowed_for_action True.")

        payload: dict[str, Any] = {
            "database_id": self.database_id,
            "properties": transition.properties,
        }
        if page_id:
            payload["page_id"] = page_id
        log = transition.as_log_dict(page_id)
        text = json.dumps(log, ensure_ascii=False, indent=2)
        if printer:
            printer("=== Payload Notion (Fila Editorial) ===")
            printer(text)
            printer("Aprovar/ações: IG=off site=off n8n=off. Nada no ar.")

        if not writes_allowed():
            msg = "Dry-run: payload impresso, Notion não foi escrito."
            if not notion_token():
                msg += " Defina NOTION_TOKEN para habilitar escrita."
            elif not confirm_env():
                msg += " Use CONFIRM=1 para escrever."
            return ActionResult(
                dry_run=True,
                written=False,
                published=False,
                n8n_fired=False,
                instagram_posted=False,
                payload=payload,
                message=msg,
                transition=transition,
            )

        if creating:
            self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=transition.properties,
            )
            message = "Card criado na Fila Editorial (Canal = Não publicar)."
        else:
            self.client.pages.update(
                page_id=page_id, properties=transition.properties
            )
            message = "Card atualizado na Fila Editorial (Notion SSOT). Não publicado."

        return ActionResult(
            dry_run=False,
            written=True,
            published=False,
            n8n_fired=False,
            instagram_posted=False,
            payload=payload,
            message=message,
            transition=transition,
        )

    def _normalize_page(self, page: dict[str, Any]) -> dict[str, Any]:
        props = page.get("properties") or {}
        peca = _title(props.get("Peça"))
        metrica = _rich(props.get("Métrica"))
        observacoes = _rich(props.get("Observações"))
        proxima = _rich(props.get("Próxima ação"))
        issues = scan_card(
            peca=peca,
            metrica=metrica,
            observacoes=observacoes,
            proxima_acao=proxima,
        )
        page_id = page.get("id") or ""
        braco = _select(props.get("Braço"))
        return {
            "id": page_id,
            "url": page.get("url") or notion_page_url(page_id),
            "peca": peca,
            "name": peca,
            "status": _select(props.get("Status")),
            "braco": braco,
            "porta": _select(props.get("Porta")),
            "formato": _select(props.get("Formato")),
            "canal": _select(props.get("Canal")),
            "metrica": metrica,
            "proxima_acao": proxima,
            "observacoes": observacoes,
            "automacao": _checkbox(props.get("Automação executada")),
            "numero": _unique_id(props.get("Nº")),
            "agente": {"Editora": "Acervo", "Produtora": "Comunicação"}.get(
                braco or ""
            ),
            "canon_issues": [
                {"code": i.code, "message": i.message, "field": i.field}
                for i in issues
            ],
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
    return "".join(
        p.get("plain_text") or p.get("text", {}).get("content") or ""
        for p in parts
    )


def _rich(prop: dict[str, Any] | None) -> str:
    if not prop:
        return ""
    parts = prop.get("rich_text") or []
    return "".join(
        p.get("plain_text") or p.get("text", {}).get("content") or ""
        for p in parts
    )


def _checkbox(prop: dict[str, Any] | None) -> bool:
    if not prop:
        return False
    return bool(prop.get("checkbox"))


def _unique_id(prop: dict[str, Any] | None) -> str | None:
    if not prop:
        return None
    uid = prop.get("unique_id") or {}
    number = uid.get("number")
    if number is None:
        # fallback se a API antiga devolver número puro
        if prop.get("number") is not None:
            return f"EDI-{prop['number']}"
        return _rich(prop) or None
    prefix = uid.get("prefix") or "EDI"
    return f"{prefix}-{number}"


def log_to_stderr(message: str) -> None:
    print(message, file=sys.stderr)
