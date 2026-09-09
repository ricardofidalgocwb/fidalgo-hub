# Testes / CI — COM-PDF-APR-N0

Pasta visível no artefato: [`tests/`](./tests/).

A guarda pytest **permanece** em `tests/test_com_pdf_apr_n0.py` (raiz do repo). Não mover.

CI (`founder_panel_tests`):

```bash
python -m pytest tests/test_com_pdf_apr_n0.py
```

Na prática o job corre `python -m pytest tests/ -q` a partir da raiz. Path de push também inclui `docs/propostas/COM-PDF-APR-N0/**`.

Local (raiz do repo):

```bash
python -m pytest tests/test_com_pdf_apr_n0.py -q
```

A guarda cobre Gold / Quiz / bans (Gold v1.1, Quiz D1 sem ✅ no enunciado, PII/nomes/Type 3). O ficheiro inclui COS P0 + P1 (gabarito `1A · 2B · 3C · 4A · 5B · 6C · 7A · 8B · 9C · 10A` em `#gabarito-d1` com `break-before: page`; mini-trilha; Progresso A1–A6) + fichas N0-H1 / N0-H2 / N0-H3 + checklist ☐ + slot A.8 Drive par dínamo+alt (443360 / 141153; heritagestocks `113903021C` · appletreekit `55A kit`; Drive IDs no HTML/README/SOURCES; Commons secundário) + caixa 12 CIP1 + caixa 8 appletreeauto 61–66 (Acervo) (≥100 KB; sem CIP1 caixa 8) + CTA didático. Sem inventar PN/assets. Não publicar. Não mover `tests/test_com_pdf_apr_n0.py` para dentro deste pacote.
