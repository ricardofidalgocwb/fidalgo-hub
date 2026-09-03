"""Canon da mesa editorial. Recusa mito e métrica inflada.

Fonte: Mesa editorial (Notion) + spec Heros Custom. Fatos travados — não inventar.
12 V no Brasil = 1968 (não 1967); 12 V não implica alternador.
Fim de linha BR = 1996 (2003 é México).
Anchieta nacional = 03/01/1959; planta Anchieta = 18/11/1959.
Ipiranga CKD = 2.268 Sedan; Itamar = 47.700.
NAP pública = 439; 557 é clube.
Figura fora desta lista é recusada, não aceita em silêncio.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

CANON_12V_YEAR = 1968
CANON_FIM_BR_YEAR = 1996
CANON_MEXICO_YEAR = 2003
CANON_ANCHIETA_YEAR = 1959
CANON_ANCHIETA_NACIONAL = "03/01/1959"
CANON_ANCHIETA_PLANTA = "18/11/1959"
CANON_NAP_PUBLIC = "439"
CANON_NAP_CLUBE = "557"
CANON_IPIRANGA_CKD = 2268
CANON_ITAMAR = 47700

# Volumes / anos / NAP já cravados. Qualquer outro número “grande” é inventado.
CANON_VOLUMES = frozenset({CANON_IPIRANGA_CKD, CANON_ITAMAR})
CANON_FIGURES = frozenset(
    {
        CANON_12V_YEAR,
        CANON_FIM_BR_YEAR,
        CANON_MEXICO_YEAR,
        CANON_ANCHIETA_YEAR,
        CANON_IPIRANGA_CKD,
        CANON_ITAMAR,
        int(CANON_NAP_PUBLIC),
        int(CANON_NAP_CLUBE),
    }
)

MYTH_12V_1967 = "12V=1967 é mito. Canônico: 12 V = 1968."
MYTH_12V_ALTERNATOR = "12 V não implica alternador."
MYTH_FIM_BR_2003 = "fim BR=2003 é mito. Canônico: fim BR = 1996 (México = 2003)."
MYTH_ANCHIETA = (
    f"Anchieta nacional = {CANON_ANCHIETA_NACIONAL}; "
    f"planta Anchieta = {CANON_ANCHIETA_PLANTA}."
)
RULE_NO_OS_CPF = "Sem OS viva e sem CPF em peça editorial."
RULE_NO_INVENTED_VOLUME = "Métrica não pode inventar volume de produção."
RULE_NAP = "NAP pública = 439. 557 é clube. Não copiar NAP EF/FSE."

_RE_12V_1967 = re.compile(
    r"12\s*v.{0,20}1967|1967.{0,20}12\s*v",
    re.IGNORECASE | re.DOTALL,
)
_RE_12V_ALTERNATOR = re.compile(
    r"12\s*v.{0,28}(implica|impl[ií]ca|=|é|significa|com)\s+alternador"
    r"|alternador.{0,28}12\s*v",
    re.IGNORECASE | re.DOTALL,
)
_RE_12V_ALTERNATOR_NEGATED = re.compile(
    r"n[aã]o\s+(implica|impl[ií]ca|é|significa)",
    re.IGNORECASE,
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
_RE_FIGURE = re.compile(r"\b\d{1,3}(?:\.\d{3})+\b|\b\d{4,}\b")
_RE_EF_NAP = re.compile(
    r"(br[- ]?116|13238|3333[- ]?8644|99979[- ]?3395)",
    re.IGNORECASE,
)
_RE_557_AS_PUBLIC = re.compile(
    r"(nap|endere[cç]o|oficina|p[uú]blic).{0,24}557|557.{0,24}(nap|endere[cç]o|oficina)",
    re.IGNORECASE | re.DOTALL,
)
_RE_ANCHIETA_YEAR = re.compile(
    r"anchieta.{0,40}(\d{4})|(\d{4}).{0,40}anchieta",
    re.IGNORECASE | re.DOTALL,
)
_RE_ANCHIETA_NACIONAL_WRONG = re.compile(
    r"(nacional|primeiro|1[oº°]\s*fusca)\D{0,16}18\s*/\s*11",
    re.IGNORECASE,
)
_RE_ANCHIETA_PLANTA_WRONG = re.compile(
    r"(planta|f[aá]brica)\D{0,16}0?3\s*/\s*0?1",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class CanonIssue:
    code: str
    message: str
    field: str


def _parse_int(raw: str) -> int | None:
    digits = re.sub(r"[.\s]", "", raw)
    if not digits.isdigit():
        return None
    return int(digits)


def issues_as_dicts(issues: list[CanonIssue]) -> list[dict[str, str]]:
    return [{"code": i.code, "message": i.message, "field": i.field} for i in issues]


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
        if _RE_12V_ALTERNATOR.search(text) and not _RE_12V_ALTERNATOR_NEGATED.search(
            text
        ):
            issues.append(CanonIssue("myth_12v_alternator", MYTH_12V_ALTERNATOR, field))
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
        issues.extend(_anchieta_issues(text, field))

        if field == "Métrica":
            issues.extend(_volume_issues(text, field))

    return issues


def _anchieta_issues(text: str, field: str) -> list[CanonIssue]:
    found: list[CanonIssue] = []
    for match in _RE_ANCHIETA_YEAR.finditer(text):
        year = int(match.group(1) or match.group(2))
        if year != CANON_ANCHIETA_YEAR:
            found.append(CanonIssue("myth_anchieta", MYTH_ANCHIETA, field))
            break
    if _RE_ANCHIETA_NACIONAL_WRONG.search(text) or _RE_ANCHIETA_PLANTA_WRONG.search(
        text
    ):
        found.append(CanonIssue("myth_anchieta", MYTH_ANCHIETA, field))
    return found


def _volume_issues(text: str, field: str) -> list[CanonIssue]:
    found: list[CanonIssue] = []
    if _RE_VOLUME.search(text):
        found.append(CanonIssue("volume_inventado", RULE_NO_INVENTED_VOLUME, field))
        return found
    for match in _RE_VOLUME_NUMBER.finditer(text):
        number = _parse_int(match.group(2))
        if number is None:
            continue
        if number in CANON_FIGURES:
            continue
        found.append(CanonIssue("volume_inventado", RULE_NO_INVENTED_VOLUME, field))
        return found
    for match in _RE_FIGURE.finditer(text):
        number = _parse_int(match.group(0))
        if number is None:
            continue
        if number in CANON_FIGURES:
            continue
        found.append(CanonIssue("volume_inventado", RULE_NO_INVENTED_VOLUME, field))
        break
    return found


def assert_card_canon(**kwargs: str | None) -> None:
    from dashboard.editorial_status import EditorialError

    issues = scan_card(
        peca=kwargs.get("peca") or "",
        metrica=kwargs.get("metrica") or "",
        observacoes=kwargs.get("observacoes") or "",
        proxima_acao=kwargs.get("proxima_acao") or "",
    )
    if not issues:
        return
    parts = [f"{i.field}: {i.message}" for i in issues]
    raise EditorialError("Canon recusado — " + " | ".join(parts))


def canon_summary() -> dict[str, object]:
    return {
        "12v": CANON_12V_YEAR,
        "12v_implica_alternador": False,
        "fim_br": CANON_FIM_BR_YEAR,
        "mexico": CANON_MEXICO_YEAR,
        "anchieta_nacional": CANON_ANCHIETA_NACIONAL,
        "anchieta_planta": CANON_ANCHIETA_PLANTA,
        "nap_publica": CANON_NAP_PUBLIC,
        "nap_clube": CANON_NAP_CLUBE,
        "volumes": sorted(CANON_VOLUMES),
        "figures": sorted(CANON_FIGURES),
    }
