# Aulas N0 A1–A6 — player unpublished

Player/páginas das seis aulas N0 (elétrica simples Type 1) em
`sites/heros-custom/aulas/`. **Irmão do MVP** de agendamento — não é publish.

Trilha irmã Cap.2 / Fusca Passaporte P0: [`cap2/`](cap2/) (F-P0-1…6).
Sub-nav nas páginas de aulas: **N0 | Cap.2 / Passaporte P0**. Header **Aulas** intacto.

**Status:** unpublished. Banner `UNPUBLISHED · DRAFT · Founder OK required to go live`.
`meta robots noindex, nofollow`. Sem domínio. Sem YouTube / Vimeo / Hotmart / n8n.

Roteiros SSOT (COM):
[COM- · Roteiros videoaula N0 A1–A6 · P0 unpublished](https://app.notion.com/p/3da7d36bae6481d098e2f5e59e89e1d0)
(`HUB-videoaula-roteiros-p0-1309`).

O miolo do aluno **não** cita este URL, nem jargão de Staff.

## Rotas

| Página | Path |
|--------|------|
| Índice A1–A6 | `/aulas/` |
| A1 Energia zero | `/aulas/a1/` |
| A2 Ano e 6 V / 12 V | `/aulas/a2/` |
| A3 12 V ≠ alternador | `/aulas/a3/` |
| A4 Diagrama e caixa | `/aulas/a4/` |
| A5 Massas primeiro | `/aulas/a5/` |
| A6 Multímetro parado | `/aulas/a6/` |

Cada aula: placeholder de player («vídeo em elaboração · unpublished») + arco
O quê · Por quê · Como · Cheque · Erro comum · Próximo.

Sem iframe. Sem URL de MP4 inventada.

## Tipadas (bytes exactos, sem recomprimir)

Copiadas de `docs/propostas/COM-PDF-APR-N0/assets/`:

| Aula | Ficheiro | Bytes | Legenda humana |
|------|----------|------:|----------------|
| A3 | `assets/N0_A8_dinam_SRC-heritagestocks.jpg` | 443360 | isto é dínamo |
| A3 | `assets/N0_A8_alt_SRC-appletreekit.jpg` | 141153 | isto é alternador |
| A4 | `assets/N0_caixa8_fuseBox8polos_SRC-appletree.jpg` | 129434 | 8 pólos |
| A4 | `assets/N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg` | 239795 | 12 pólos |

A1, A2, A5 e A6 ficam com still textual — sem foto de stock inventada.

Legendas no miolo são humanas. IDs de Drive ficam **fora** das captions.

## Local

```bash
cd sites/heros-custom
python3 -m http.server 4174 --bind 127.0.0.1
```

http://127.0.0.1:4174/aulas/

## Guarda

`tests/test_n0_aulas_player.py`

Miolo do aluno: sem R$, sem NAP, sem WhatsApp, sem OS viva, sem Hotmart.
Merge = Founder.
