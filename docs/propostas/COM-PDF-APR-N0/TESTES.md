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

**8 testes** da guarda original cobrem Gold / Quiz / bans (Gold v1.1, Quiz D1 sem ✅ no enunciado, PII/nomes/Type 3). O ficheiro inclui COS P0 + fichas N0-H1 / N0-H2 / N0-H3 + checklist ☐ + slot A.8 Commons + caixa 12 CIP1 (≥100 KB; caixa 8 AUSENTE) + CTA didático. Não publicar. Não mover `tests/test_com_pdf_apr_n0.py` para dentro deste pacote.
