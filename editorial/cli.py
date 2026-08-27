"""CLI da mesa editorial. Dry-run por padrão. Não publica."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from editorial.ids import fila_editorial
from editorial.notion_fila import (
    NotionEditorialClient,
    confirm_env,
    notion_token,
    writes_allowed,
)
from editorial.pulse import build_pulse
from editorial.status_machine import ACTION_NOVO, TransitionError

load_dotenv()

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixtures" / "sample_fila.json"


def _load_cards() -> tuple[list[dict], str]:
    token = notion_token()
    if not token:
        if FIXTURE.exists():
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            return data, "demonstração (sem NOTION_TOKEN)"
        return [], "sem token e sem fixture"
    try:
        cards = NotionEditorialClient().query_cards()
        return cards, "live Notion"
    except Exception as exc:  # noqa: BLE001 — CLI interno
        if FIXTURE.exists():
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            return data, f"fixture (falha live: {exc})"
        raise


def _print_pulse(pulse: dict, source: str) -> None:
    cfg = fila_editorial()
    print("Mesa editorial · Editora × Produtora · Heros Custom")
    print(f"Fonte: {source}")
    print(f"Fila: {cfg['url']}")
    print(f"Mesa: {cfg['mesa_url']}")
    dry = "ligado" if not writes_allowed() else "liberado via CONFIRM=1"
    print(f"Dry-run: {dry}")
    print("Aprovar NUNCA publica (IG/site/n8n). Publicado só o Founder marca.")
    print("Agentes: Acervo (Editora) · Comunicação (Produtora). Sem AGT-09.")
    print()
    print("Por Status:")
    for status, n in pulse["counts"].items():
        print(f"  {status}: {n}")
    print("Por Braço:")
    for braco, n in pulse["por_braco"].items():
        print(f"  {braco}: {n}")
    proximo = pulse.get("proximo")
    print()
    if proximo:
        print("Próximo Aguardando OK:")
        print(f"  {proximo.get('numero') or '—'} · {proximo.get('peca')}")
        print(f"  Braço: {proximo.get('braco')} → {proximo.get('agente')}")
        print(f"  Canal: {proximo.get('canal')} · Formato: {proximo.get('formato')}")
        print(f"  {proximo.get('url')}")
    else:
        print("Nenhum card em Aguardando OK.")
    alertas = pulse.get("canon_alertas") or []
    if alertas:
        print()
        print("Alertas de canon:")
        for card in alertas:
            print(f"  {card.get('peca')}: {card.get('canon_issues')}")


def cmd_pulse(_args: argparse.Namespace) -> int:
    cards, source = _load_cards()
    _print_pulse(build_pulse(cards), source)
    return 0


def _card_by_id(page_id: str) -> dict | None:
    cards, _source = _load_cards()
    compact = page_id.replace("-", "").lower()
    for card in cards:
        cid = (card.get("id") or "").replace("-", "").lower()
        if cid == compact:
            return card
    return None


def cmd_action(args: argparse.Namespace) -> int:
    page_id = getattr(args, "page_id", None)
    card = _card_by_id(page_id) if page_id else None
    current = getattr(args, "status", None) or (card or {}).get("status")
    try:
        result = NotionEditorialClient().apply_action(
            args.action,
            page_id=page_id,
            current_status=current,
            reason=getattr(args, "reason", None),
            peca=getattr(args, "peca", None) or (card or {}).get("peca"),
            metrica=getattr(args, "metrica", None) or (card or {}).get("metrica"),
            observacoes=(card or {}).get("observacoes"),
            proxima_acao=(card or {}).get("proxima_acao"),
            braco=getattr(args, "braco", None),
            porta=getattr(args, "porta", None),
            formato=getattr(args, "formato", None),
        )
    except TransitionError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2
    print(result.message)
    print(f"dry_run={result.dry_run} written={result.written} "
          f"published={result.published} instagram={result.instagram_posted} "
          f"n8n={result.n8n_fired}")
    print(f"to_status={result.transition.to_status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Mesa editorial Heros Custom — pulso e Aprovar/Recusar/Adiar. "
            "Dry-run padrão. Não publica."
        )
    )
    sub = parser.add_subparsers(dest="action", required=True)

    p_pulse = sub.add_parser("pulse", help="Contagens por Status/Braço + próximo OK")
    p_pulse.set_defaults(func=cmd_pulse)

    p_ok = sub.add_parser("aprovar", help="Rascunho/Aguardando OK → Aprovado (não publica)")
    p_ok.add_argument("page_id")
    p_ok.add_argument("--status", help="Status atual se não houver leitura live")
    p_ok.add_argument("--peca")
    p_ok.add_argument("--metrica")
    p_ok.set_defaults(func=cmd_action)

    p_no = sub.add_parser("recusar", help="→ Recusado (exige --reason)")
    p_no.add_argument("page_id")
    p_no.add_argument("--status")
    p_no.add_argument("--reason", required=True)
    p_no.set_defaults(func=cmd_action)

    p_wait = sub.add_parser("adiar", help="Volta a Rascunho (schema sem Adiado)")
    p_wait.add_argument("page_id")
    p_wait.add_argument("--status")
    p_wait.add_argument("--reason")
    p_wait.set_defaults(func=cmd_action)

    p_new = sub.add_parser("novo", help="Cria card em Rascunho, Canal=Não publicar")
    p_new.add_argument("--peca", required=True)
    p_new.add_argument("--braco", required=True, choices=["Editora", "Produtora"])
    p_new.add_argument(
        "--formato",
        required=True,
        choices=["Almanaque", "Módulo", "Ficha", "Reel", "Carrossel", "Post"],
    )
    p_new.add_argument("--porta", default="Interno", choices=["Venda", "Clube", "Interno"])
    p_new.add_argument("--metrica")
    p_new.set_defaults(action=ACTION_NOVO, func=cmd_action)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        argv = ["pulse"]
    parser = build_parser()
    args = parser.parse_args(argv)
    if os.getenv("CONFIRM", "").strip() == "1" and not notion_token():
        print("CONFIRM=1 sem NOTION_TOKEN: continua dry-run.", file=sys.stderr)
    if confirm_env() and notion_token():
        print("CONFIRM=1: escrita Notion habilitada (ainda sem publicar).", file=sys.stderr)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
