"""Runner editorial — Fila Editora × Produtora (Heros).

Dry-run é o padrão: imprime a fila e o PATCH planejado, não escreve no Notion
e não POST em lugar nenhum. CONFIRM=1 + token só atualiza Status=Aprovado
(e talvez Observações). Aprovar ≠ publicar.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

from dashboard.editorial_canon import canon_summary, issues_as_dicts, scan_card
from dashboard.editorial_status import (
    ACTION_APROVAR,
    ACTION_RECUSAR,
    APPROVABLE_STATUSES,
    CANAL_NAO_PUBLICAR,
    PIPELINE_STATUSES,
    RULE_APROVAR_NAO_PUBLICA,
    EditorialError,
    EditorialTransition,
    assert_editorial_database_only,
    assert_editorial_only_payload,
    assert_n8n_never,
    assert_never_publicado,
    build_transition,
    empty_counts,
    n8n_allowed_for_editorial_action,
)
from dashboard.ids import fila_editorial

load_dotenv()

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixtures" / "sample_fila_editorial.json"
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")


def notion_token() -> str | None:
    token = (os.getenv("NOTION_TOKEN") or "").strip()
    return token or None


def confirm_env() -> bool:
    return os.getenv("CONFIRM", "").strip() == "1"


def writes_allowed() -> bool:
    """Escreve só com token E CONFIRM=1. Sem UI neste runner."""
    return bool(notion_token()) and confirm_env()


@dataclass
class ActionResult:
    dry_run: bool
    written: bool
    n8n_fired: bool
    publish: bool
    payload: dict[str, Any]
    message: str
    transition: EditorialTransition


class EditorialClient:
    """Cliente estreito: consulta a Fila Editorial e, com CONFIRM=1, PATCHa Status."""

    def __init__(self, client: Any | None = None) -> None:
        self._cfg = fila_editorial()
        self.database_id = self._cfg["database_id"]
        self._client = client
        if self._cfg.get("write"):
            raise EditorialError(
                "fila_editorial.write deve permanecer false. "
                "Escrita só via este runner (runner_only) com CONFIRM=1."
            )
        if not self._cfg.get("runner_only"):
            raise EditorialError("Fila Editorial é runner-only.")
        assert_editorial_database_only(self.database_id)

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
        assert_editorial_database_only(self.database_id)
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
        canal: str | None = None,
        peca: str | None = None,
        metrica: str | None = None,
        observacoes: str | None = None,
        proxima_acao: str | None = None,
        printer: Callable[[str], None] | None = print,
    ) -> ActionResult:
        assert_editorial_database_only(self.database_id)
        if n8n_allowed_for_editorial_action(action):
            raise EditorialError("Runner editorial nunca dispara n8n.")

        transition = build_transition(
            action,
            current_status,
            reason=reason,
            canal=canal,
            peca=peca,
            metrica=metrica,
            observacoes=observacoes,
            proxima_acao=proxima_acao,
        )
        assert_editorial_only_payload(transition.properties)
        assert_never_publicado(transition.properties)
        assert_n8n_never(transition)

        payload = {
            "page_id": page_id,
            "database_id": self.database_id,
            "properties": transition.properties,
            "canal_unchanged": transition.canal_unchanged,
            "publish": False,
            "fire_n8n": False,
        }
        log = transition.as_log_dict(page_id)
        text = json.dumps(log, ensure_ascii=False, indent=2)
        if printer:
            printer("=== Payload Notion (Fila Editorial) ===")
            printer(text)
            printer(RULE_APROVAR_NAO_PUBLICA)

        dry = not writes_allowed()
        if dry:
            msg = "Dry-run: payload impresso, Notion não foi escrito. Sem n8n/IG/PDF/site."
            if not notion_token():
                msg += " Defina NOTION_TOKEN para habilitar escrita."
            elif not confirm_env():
                msg += " Use CONFIRM=1 para gravar só Status=Aprovado (Aprovar ≠ publicar)."
            return ActionResult(
                dry_run=True,
                written=False,
                n8n_fired=False,
                publish=False,
                payload=payload,
                message=msg,
                transition=transition,
            )

        self.client.pages.update(page_id=page_id, properties=transition.properties)
        if action == ACTION_APROVAR and printer:
            printer("Aprovar: Status=Aprovado. Canal intacto. Publicado não foi definido.")

        return ActionResult(
            dry_run=False,
            written=True,
            n8n_fired=False,
            publish=False,
            payload=payload,
            message="Peça atualizada na Fila Editorial (Status apenas). Não publicada.",
            transition=transition,
        )

    def _normalize_page(self, page: dict[str, Any]) -> dict[str, Any]:
        props = page.get("properties") or {}
        numero, codigo = _unique_id(props.get("Nº"))
        peca = _title(props.get("Peça"))
        page_id = page.get("id") or ""
        url = page.get("url") or notion_page_url(page_id)
        return {
            "id": page_id,
            "url": url,
            "peca": peca,
            "numero": numero,
            "codigo": codigo,
            "status": _select(props.get("Status")),
            "braco": _select(props.get("Braço")),
            "canal": _select(props.get("Canal")),
            "formato": _select(props.get("Formato")),
            "porta": _select(props.get("Porta")),
            "metrica": _text(props.get("Métrica")),
            "observacoes": _text(props.get("Observações")),
            "proxima_acao": _text(props.get("Próxima ação")),
            "data": _date(props.get("Data")),
            "automacao_executada": _checkbox(props.get("Automação executada")),
        }


def notion_page_url(page_id: str) -> str:
    compact = (page_id or "").replace("-", "")
    return f"https://www.notion.so/{compact}"


def load_cards() -> tuple[list[dict[str, Any]], str]:
    token = notion_token()
    if not token:
        return _load_fixture(), "demonstração (sem NOTION_TOKEN)"
    try:
        return EditorialClient().query_cards(), "live Notion"
    except Exception as exc:  # noqa: BLE001 — runner interno, cai no fixture
        return _load_fixture(), f"fixture (falha live: {exc})"


def _load_fixture() -> list[dict[str, Any]]:
    if not FIXTURE.exists():
        return []
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def build_dry_run_report(cards: list[dict[str, Any]], source: str) -> dict[str, Any]:
    cfg = fila_editorial()
    counts = empty_counts()
    for card in cards:
        status = card.get("status") or ""
        if status in counts:
            counts[status] += 1
    planned: list[dict[str, Any]] = []
    canon_blocked: list[dict[str, Any]] = []
    for card in cards:
        status = (card.get("status") or "").strip()
        if status not in APPROVABLE_STATUSES:
            continue
        issues = scan_card(
            peca=card.get("peca") or "",
            metrica=card.get("metrica") or "",
            observacoes=card.get("observacoes") or "",
            proxima_acao=card.get("proxima_acao") or "",
        )
        if issues:
            canon_blocked.append(
                {
                    "page_id": card.get("id"),
                    "peca": card.get("peca"),
                    "codigo": card.get("codigo"),
                    "from_status": status,
                    "canon_issues": issues_as_dicts(issues),
                }
            )
            continue
        transition = build_transition(
            ACTION_APROVAR,
            status,
            canal=card.get("canal") or CANAL_NAO_PUBLICAR,
            peca=card.get("peca"),
            metrica=card.get("metrica"),
            observacoes=card.get("observacoes"),
            proxima_acao=card.get("proxima_acao"),
        )
        item = transition.as_log_dict(card.get("id"))
        item["peca"] = card.get("peca")
        item["codigo"] = card.get("codigo")
        planned.append(item)
    return {
        "dry_run": True,
        "written": False,
        "n8n_fired": False,
        "publish": False,
        "source": source,
        "database_id": cfg["database_id"],
        "data_source_id": cfg.get("data_source_id"),
        "write": False,
        "runner_only": True,
        "rule": RULE_APROVAR_NAO_PUBLICA,
        "statuses": list(PIPELINE_STATUSES),
        "counts": counts,
        "canon": canon_summary(),
        "queue": cards,
        "planned": planned,
        "canon_blocked": canon_blocked,
    }


def find_card(cards: list[dict[str, Any]], page_id: str) -> dict[str, Any] | None:
    wanted = (page_id or "").replace("-", "").lower()
    for card in cards:
        cid = (card.get("id") or "").replace("-", "").lower()
        codigo = (card.get("codigo") or "").strip().upper()
        if cid == wanted or codigo == page_id.strip().upper():
            return card
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Runner editorial — Editora × Produtora (Heros). "
            "Dry-run padrão. Aprovar ≠ publicar."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Lista a fila e as transições planejadas (padrão se nenhuma ação).",
    )
    parser.add_argument(
        "--approve",
        metavar="PAGE_ID",
        help="Aprovar peça (Rascunho/Aguardando OK → Aprovado). Dry-run sem CONFIRM=1.",
    )
    parser.add_argument(
        "--refuse",
        metavar="PAGE_ID",
        help="Recusar peça (→ Recusado). Dry-run sem CONFIRM=1.",
    )
    parser.add_argument("--reason", help="Observação (aprovar) ou motivo (recusar).")
    parser.add_argument(
        "--status",
        help="Status atual se o card não estiver na fila carregada.",
    )
    args = parser.parse_args(argv)

    if args.approve and args.refuse:
        print("Use só --approve ou --refuse.", file=sys.stderr)
        return 2

    cards, source = load_cards()

    if args.approve or args.refuse:
        page_id = args.approve or args.refuse
        action = ACTION_APROVAR if args.approve else ACTION_RECUSAR
        card = find_card(cards, page_id)
        current = (args.status or (card or {}).get("status") or "").strip()
        canal = (card or {}).get("canal") or CANAL_NAO_PUBLICAR
        if not current:
            print(
                f"Peça {page_id} sem status. Passe --status ou use um id da fila.",
                file=sys.stderr,
            )
            return 1
        resolved_id = (card or {}).get("id") or page_id
        try:
            result = EditorialClient().apply_action(
                resolved_id,
                action,
                current,
                reason=args.reason,
                canal=canal,
                peca=(card or {}).get("peca"),
                metrica=(card or {}).get("metrica"),
                observacoes=(card or {}).get("observacoes"),
                proxima_acao=(card or {}).get("proxima_acao"),
            )
        except EditorialError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(result.message)
        print(
            json.dumps(
                {
                    "ok": True,
                    "dry_run": result.dry_run,
                    "written": result.written,
                    "n8n_fired": result.n8n_fired,
                    "publish": result.publish,
                    "to_status": result.transition.to_status,
                    "payload": result.payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    report = build_dry_run_report(cards, source)
    print("=== Fila Editorial — Editora × Produtora (dry-run) ===")
    print(RULE_APROVAR_NAO_PUBLICA)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


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


def _text(prop: dict[str, Any] | None) -> str:
    if not prop:
        return ""
    parts = prop.get("rich_text") or prop.get("text") or []
    if isinstance(parts, str):
        return parts
    return "".join(p.get("plain_text") or p.get("text", {}).get("content") or "" for p in parts)


def _date(prop: dict[str, Any] | None) -> str | None:
    if not prop:
        return None
    date = prop.get("date")
    if not date:
        return None
    return date.get("start")


def _checkbox(prop: dict[str, Any] | None) -> bool:
    if not prop:
        return False
    return bool(prop.get("checkbox"))


def _unique_id(prop: dict[str, Any] | None) -> tuple[int | None, str | None]:
    if not prop:
        return None, None
    uid = prop.get("unique_id")
    if not uid:
        return None, None
    number = uid.get("number")
    prefix = (uid.get("prefix") or "").strip()
    if number is None:
        return None, None
    codigo = f"{prefix}-{number}" if prefix else str(number)
    return number, codigo


if __name__ == "__main__":
    sys.exit(main())
