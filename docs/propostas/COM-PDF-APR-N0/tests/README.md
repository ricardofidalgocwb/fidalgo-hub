# Testes deste pacote

A guarda pytest **não** vive nesta pasta. O ficheiro canónico está na raiz do repo:

`tests/test_com_pdf_apr_n0.py`

(caminho absoluto no clone: `/tests/test_com_pdf_apr_n0.py` a partir da raiz do Hub.)

## CI

O workflow `founder_panel_tests` corre, a partir da **raiz do repositório**:

```bash
python -m pytest tests/test_com_pdf_apr_n0.py
```

Na prática o job executa `python -m pytest tests/ -q`, que inclui este ficheiro (e o resto de `tests/`). **Não** mover a guarda para `docs/propostas/COM-PDF-APR-N0/tests/`.

## Local (raiz do repo)

```bash
python -m pytest tests/test_com_pdf_apr_n0.py -q
```

A guarda cobre Gold v1.1, Quiz D1 (sem ✅ no enunciado), ☐ do checklist, slot A.8 Commons + caixa 12 CIP1 + caixa 8 appletree (≥100 KB; sem CIP1 caixa 8), CTA sem NAP/WhatsApp, e bans (Theodoro / Diogo / CPF / OS viva).

`test_path.py` aqui só confirma que o ficheiro da raiz existe — corra-o a partir da raiz:

```bash
python -m pytest docs/propostas/COM-PDF-APR-N0/tests/test_path.py -q
```
