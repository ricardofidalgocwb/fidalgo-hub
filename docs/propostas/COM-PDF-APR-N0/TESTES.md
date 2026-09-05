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

A guarda cobre Gold v1.1, Quiz D1 (sem ✅ no enunciado; gabarito só no fim), checklist ☐, slots AUSENTE, fichas N0-H1 / N0-H2 / N0-H3, CTA didático e bans (Theodoro / Diogo / CPF / OS viva / Type 3 como ensino). Não publicar.
