"""Sincronismo canônico da mesa editorial. Recusa mito e métrica inflada.

Fonte: Mesa editorial (Notion) + spec Heros Custom.
12 V = 1968 · fim BR = 1996 · México = 2003 · NAP pública 439.
Sem OS viva, sem CPF, sem volume inventado.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

CANON_12V_YEAR = 1968
CANON_FIM_BR_YEAR = 1996
CANON_MEXICO_YEAR = 2003
CANON_NAP_PUBLIC = "439"
CANON_NAP_CLUBE = "557"

# Volumes que a mesa já cravou (não inflar).
CANON_VOLUMES = frozenset({2268, 47700})

MYTH_12V_1967 = "12V=1967 é mito. Canônico: 12 V = 1968."
MYTH_FIM_BR_2003 = "fim BR=2003 é mito. Canônico: fim BR = 1996 (México = 2003)."
RULE_NO_OS_CPF = "Sem OS viva e sem CPF em peça editorial."
RULE_NO_INVENTED_VOLUME = "Métrica não pode inventar volume de produção."
RULE_NAP = "NAP pública = 439. 557 é clube. Não copiar NAP EF/FSE."

_RE_12V_1967 = re.compile(
    r"12\s*v.{0,20}1967|1967.{0,20}12\s*v",
    re.IGNORECASE | re.DOTALL,
)
_RE_FIM_BR_2003 = re.compile(
    r"(fim\s*(de\s*)?(br|brasil)\s*[=:]?\s*2003|"
    r"2003\s*[=:]?\s*fim\s*(de\s*)?(br|brasil)|"
    r"(?<!m[eé]xico\s)(?<!mx\s)\bbr\s*=\s*2003\b)",
    re.IGNORECASE,
)
_RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
_RE_LIVE_OS = re.compile(
    r"(\bos[- ]\d{2,}\b|\bhc[- ]?\d{4}[- ]\d{3,}\b|(?<!sem )(?<!sem\s)\bos\s+viva\b)",
    re.IGNORECASE,
)
_RE_VOLUME = re.compile(
    r"("
    r"\d[\d.\s]*\s*(milh[oõ]es|mi\b)"
    r"|volume\s+(de\s+)?produ[cç][aã]o"
    r"|unidades\s+produz"
    r"|produzidos?\s*[:\-]?\s*\d{4,}"
    r")",
    re.IGNORECASE,
)
_RE_VOLUME_NUMBER = re.compile(
    r"(produ[cç][aã]o|produzidos?|unidades|volume)\D{0,12}(\d[\d.]{2,})",
    re.IGNORECASE,
)
_RE_EF_NAP = re.compile(
    r"(br[- ]?116|13238|3333[- ]?8644|99979[- ]?3395)",
    re.IGNORECASE,
)
_RE_557_AS_PUBLIC = re.compile(
    r"(nap|endere[cç]o|oficina|p[uú]blic).{0,24}557|557.{0,24}(nap|endere[cç]o|oficina)",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class CanonIssue:
    code: str
    message: str
    field: str


def _blob(*parts: str | None) -> str:
    return " ".join(p for p in parts if p)


def _parse_int(raw: str) -> int | None:
    digits = re.sub(r"[.\s]", "", raw)
    if not digits.isdigit():
        return None
    return int(digits)


def scan_card(
    *,
    peca: str = "",
    metrica: str = "",
    observacoes: str = "",
    proxima_acao: str = "",
) -> list[CanonIssue]:
    """Varre campos de texto. Não escreve nada."""
    issues: list[CanonIssue] = []
    fields = {
        "Métrica": metrica or "",
        "Peça": peca or "",
        "Observações": observacoes or "",
        "Próxima ação": proxima_acao or "",
    }

    for field, text in fields.items():
        if not text:
            continue
        text_os = re.sub(r"sem\s+os\s+viva", " ", text, flags=re.IGNORECASE)
        if _RE_12V_1967.search(text):
            issues.append(CanonIssue("myth_12v_1967", MYTH_12V_1967, field))
        if _RE_FIM_BR_2003.search(text) and not re.search(
            r"m[eé]xico", text, re.IGNORECASE
        ):
            issues.append(CanonIssue("myth_fim_br_2003", MYTH_FIM_BR_2003, field))
        if _RE_CPF.search(text):
            issues.append(CanonIssue("cpf", RULE_NO_OS_CPF, field))
        if _RE_LIVE_OS.search(text_os):
            issues.append(CanonIssue("os_viva", RULE_NO_OS_CPF, field))
        if _RE_EF_NAP.search(text):
            issues.append(CanonIssue("nap_cruzada", RULE_NAP, field))
        if _RE_557_AS_PUBLIC.search(text):
            issues.append(CanonIssue("nap_557_publica", RULE_NAP, field))

        if field == "Métrica":
            issues.extend(_volume_issues(text, field))

    return issues


def _volume_issues(text: str, field: str) -> list[CanonIssue]:
    found: list[CanonIssue] = []
    if _RE_VOLUME.search(text):
        found.append(
            CanonIssue("volume_inventado", RULE_NO_INVENTED_VOLUME, field)
        )
        return found
    for match in _RE_VOLUME_NUMBER.finditer(text):
        number = _parse_int(match.group(2))
        if number is None:
            continue
        if number in CANON_VOLUMES:
            continue
        if number in {CANON_12V_YEAR, CANON_FIM_BR_YEAR, CANON_MEXICO_YEAR}:
            continue
        if number == int(CANON_NAP_PUBLIC):
            continue
        found.append(
            CanonIssue("volume_inventado", RULE_NO_INVENTED_VOLUME, field)
        )
        break
    return found


def assert_card_canon(**kwargs: str | None) -> None:
    from editorial.status_machine import TransitionError

    issues = scan_card(
        peca=kwargs.get("peca") or "",
        metrica=kwargs.get("metrica") or "",
        observacoes=kwargs.get("observacoes") or "",
        proxima_acao=kwargs.get("proxima_acao") or "",
    )
    if not issues:
        return
    parts = [f"{i.field}: {i.message}" for i in issues]
    raise TransitionError("Canon recusado — " + " | ".join(parts))


def canon_summary() -> dict[str, object]:
    return {
        "12v": CANON_12V_YEAR,
        "fim_br": CANON_FIM_BR_YEAR,
        "mexico": CANON_MEXICO_YEAR,
        "nap_publica": CANON_NAP_PUBLIC,
        "nap_clube": CANON_NAP_CLUBE,
        "volumes": sorted(CANON_VOLUMES),
    }
