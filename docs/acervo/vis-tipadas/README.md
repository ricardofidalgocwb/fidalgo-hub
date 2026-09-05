# VIS tipadas H1 / VIS-G1 + M6 tronco T

**Status:** acervo interno, **não publicado**. Sem site até OK Founder. Não implantar. Não colar em N0-H1. Não misturar com Cap.2 / N0 A.8.

Pacote de **três** tipadas Commons SRC (≥100 000 bytes). TEC PASS 05/09. COS: Scout tipa → Ops Drive → Acervo indexa slot Mestra.

Este pacote **não** é curso Mód.1, **não** é PDF M6 Avançado, **não** é Variant. Sem HTML/PDF de módulo aqui — só binários + mapa de slots.

## Mapa de slots (este PR)

| Slot Mestra | Arquivo | Bytes | Onde cola | O que **não** é |
|---|---|---|---|---|
| **VIS-G1 / H1a** | `H1_VW_Beetle_1946_SRC-commons.jpg` | 512 333 | Mód.1 V-G1 · gênese / protótipos | **≠** ficha `N0-H1` Era B1 1959–66 em COM-PDF-APR-N0 |
| **VIS-G1 / H1b** | `H1_KdF_Wagen42_SRC-commons.jpg` | 434 867 | Mód.1 V-G1 · KdF / gênese | **≠** Anchieta 03/01/1959 · **≠** N0-H1 |
| **M6 tronco T** | `M6_T_motor30PS1959_SRC-commons.jpg` | 578 324 | M6 térmica (único ≠ Cap.2) | **≠** DUP `M6_T_engineBayTin` / `Cap2_engineBay` |

Citações (Commons + Drive IDs + índice VIS): [`SOURCES.md`](SOURCES.md).

## Fora deste PR (não preencher)

- Cap.2 / N0 A.8 — PR separado. Não embutir `Cap2_engineBay` nem `N0_A8_*`.
- `M6_T_engineBayTin` = **DUP-A** de Cap.2 bay — **fora**.
- HenryFord / lote-2 FAIL candidates — **fora**.
- Caixa 8 vs 12 tipada — **AUSENTE**.
- A1 HOLD — **não** preencher.
- Ficha **N0-H1 Era B1 1959–66** em `docs/propostas/COM-PDF-APR-N0/` — slot diferente; **não** sobrescrever com fotos 1940s.

Não há pacote HTML/PDF de Mód.1 ou M6 neste repo para “colar” slots. Quando existir, usar só os vazios VIS-G1 / M6_T deste mapa.

## Regras duras

- Sem publish / sem site / sem n8n
- Sem stock / IA / stub ≤100 000 bytes
- Sem Type 3 / Variant
- Sem CPF / OS viva / placa de cliente
- MCP Drive `create_file` **proibido** para binário (SSOT: [`docs/drive-binary-upload.md`](../../drive-binary-upload.md))

## Guarda CI

`tests/test_vis_tipadas_h1_m6.py` — os três ficheiros existem e `st_size >= 100000`.

*Heros Custom · Acervo · COM-VIS-H1-M6 · 05/09/2026 · não publicar*
