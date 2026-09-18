# COM-PDF-GEN-F-fusca — GEN-F Fusca gênese (1º e-book digital)

**Status:** rascunho interno 0.1, **não publicado**. Sem site até OK Founder. Não implantar. Não enviar como curso no ar. Pacote **separado** do COM-PDF-APR-N0 e do COM-PDF-CAP2-motor.

**HUB-ebook-fusca-genesis-1709** · Founder GO · camada de gênese cultural (≠ N0 elétrico · ≠ Cap.2 tinware sozinho). Taxonomia **GEN-F1…GEN-F5**.

**Aprendiz testa como aluno** — lê GEN-F1…F5, responde o Cheque 1Q/cap, marca o checklist de evidência. Não trata este PDF como publicação.

**P0 tom 17/09 (unpublished):** arco COM por capítulo (o quê → por quê → como → cheque → erro → próximo) + fio «O carro popular que atravessou gerações — e ainda pede critério, não improviso.» Miolo = você / família; sem jargão Staff/OS/Path. Sem checkout.

| Bloco | O que é | Neste PDF |
|---|---|---|
| **Capa** | Type 1 · gênese cultural · UNPUBLISHED | Completa |
| **GEN-F1** | Origem KdF → Type 1 · Type 1 ≠ Type 3 | H1a 1946 + H1b KdF (byte-exact) |
| **GEN-F2** | Por quê aircooled · ponte Cap.2 | AUR1500 + Coccinelle (byte-exact) |
| **GEN-F3** | Mobilidade família | Still textual · tipada dedicada **AUSENTE** |
| **GEN-F4** | Indústria mundo+BR · 1968 / 1996 / Itamar 93–96 | Caixa 8/12 + dínamo/alt · Anchieta foto **AUSENTE** |
| **GEN-F5** | Ponte Passaporte · CTA soft | Checklist evidência · N0-A / F-P0 · flatlay **AUSENTE** |

## O que é

1º e-book digital Type 1: **gênese cultural**. Padrão Heros. Não é N0 elétrica. Não é Cap. 2 tinware sozinho. Não é módulo Variant / Type 3.

Cânon TEC (FAIL se contradizer):

- 12 V BR = **1968** (não 1967)
- 12 V ≠ alternador
- Fim BR = **1996** (2003 = México — fora do miolo BR)
- Type 1 ≠ Type 3
- Sem cv / torque inventado
- Itamar = faixa **1993–96** (volume 47.700 = HOLD, não inventar no miolo)
- 1º nacional **03/01/1959** · planta Anchieta **18/11/1959**
- CKD Ipiranga **2.268** Sedan (Mestra Cap.1) · ≠ fábrica do nacional

## Refs internas (não vão no HTML / PDF)

Estes nomes ficam **só neste README**. Não colar URL viva de Notion nem CPF no artefato:

- COM- · Outline GEN-F Fusca gênese · 5 caps + arco · 17/09
- EDI- · Inventário GEN-F · e-book gênese Fusca · 17/09
- EDI- · Mapa GEN-F × Mestra/cite + gaps VIS · 17/09
- Cap. 1 — Do KdF-Wagen ao Type 1 (Mestra, rascunho 0.2)
- Cap. 3 — Anchieta e o Fusca nacional (1959)
- VIS tipadas H1 / VIS-G1 (docs/acervo/vis-tipadas/)
- N0 / Cap.2 = outros PDFs

## Como regenerar localmente

Fonte: `index.html` + `print.css`. Não há WeasyPrint/reportlab nas deps do Hub.

### 1. Ver no navegador

```bash
cd docs/propostas/COM-PDF-GEN-F-fusca
python3 -m http.server 4179 --bind 127.0.0.1
```

Abrir http://127.0.0.1:4179/ — **não** é deploy.

### 2. Salvar PDF (Chrome / Chromium)

Pelo diálogo: Arquivo → Imprimir → Destino **Salvar como PDF** → A4 → fundos de gráfico ligados.

Pela linha de comando:

```bash
./emitir-pdf.sh
```

Saída: `COM-PDF-GEN-F-fusca.pdf`. Um snapshot pode estar commitado nesta pasta; regenerar localmente o substitui.

Requisitos: `google-chrome` ou `chromium` no PATH. As tipadas estão em `assets/` (local; sem rede). Montserrat/Inter caem no fallback se o Google Fonts não carregar.

## Testes / CI

A guarda pytest vive na raiz do repo:

```bash
python -m pytest tests/test_com_pdf_gen_f.py
```

Workflow: `.github/workflows/founder_panel_tests.yml` (`pytest tests/` + path `docs/propostas/COM-PDF-GEN-F-fusca/**`).

## Fotos-modelo — H1 + AUR/cocc + N0 caixa/dinam/alt (unpublished)

**Status:** rascunho interno, **não publicado**. Sem site até OK Founder.

Cópias **byte-exact** dos slots Mestra já tipados. Sem stock / IA. Sem foto de Anchieta / família inventada.

| Slot | Arquivo | Bytes | Cite |
|---|---|---|---|
| GEN-F1 H1b KdF | `assets/H1_KdF_Wagen42_SRC-commons.jpg` | **434867** | Commons KdF-Wagen '42 · Drive `1Kd6Y75J_Hczhb4CuG9R9mHOfTcf4AenT` |
| GEN-F1 H1a 1946 | `assets/H1_VW_Beetle_1946_SRC-commons.jpg` | **519609** | Commons VW Beetle (1946) · Drive `1vjVvZ18DYGUREYEfYFzvadlOa3OHGwbp` |
| GEN-F2 AUR1500 | `assets/Cap2_P0_tinware_AUR1500_SRC-commons.jpg` | **483449** | Commons Engine of VW 1500 AUR 131F · Drive `1W9m0-CSUoeyLqDVafsEclQTNlUjV_qJZ` |
| GEN-F2 Coccinelle | `assets/Cap2_P0_tinware_coccinelle_SRC-commons.jpg` | **1111977** | Commons Volkswagen Coccinelle, beige (2) · Drive `1RJYn4YwIQmqERYNkpN8QMPVYu6LJYt1M` |
| GEN-F4 caixa 8 | `assets/N0_caixa8_fuseBox8polos_SRC-appletree.jpg` | **129434** | appletreeauto 61–66 · Drive `1K2IIqdAtPPysoloSFJcmfuv43zr_AlqK` |
| GEN-F4 caixa 12 | `assets/N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg` | **239795** | cip1 111 937 505 M · Drive `12Xtkudi1r-gjmKmy1QTk9pjjmMTyZZtx` |
| GEN-F4 dínamo | `assets/N0_A8_dinam_SRC-heritagestocks.jpg` | **443360** | heritagestocks · `113903021C` · Drive `1a_L6-bgoABwfW8VTeRfCA7nMg6zhUq_i` |
| GEN-F4 alternador | `assets/N0_A8_alt_SRC-appletreekit.jpg` | **141153** | appletreekit · `55A kit` · Drive `1NQx1Ef7yG5O-uoU8JRjnc1RFfS3wChAi` |

Citações: [`SOURCES.md`](SOURCES.md).

**AUSENTE / HOLD:** tipada família/rua (GEN-F3) · tipada Anchieta/fábrica BR (GEN-F4) · volume Itamar 47.700 · stamp B · flatlay F-P0 evidência (GEN-F5).

**Não embutir:** `M6_T_motor30PS1959` · `Cap2_engineBay` · `*30PS*` · `N0_caixa8*cip1` · H2/H3 inventadas · foto de cliente / stock / IA.

## Regras duras deste artefato

- Sem CPF / OS viva / placa de cliente
- Sem site até OK Founder
- Sem URL viva de Notion
- Sem Instagram
- Sem n8n
- Sem NAP / WhatsApp / checkout / Hotmart
- Sem Staff / Path no miolo
- Type 3 = outro módulo
- Sem cv / torque / folga inventados
- Sem inventar tipada Anchieta / família
- Pacote separado do N0 e do Cap.2

## Marca

Heros Custom · Gold v1.1 (COM-ALIGN-01) · Montserrat (títulos) + Inter (corpo).

| Token | HEX |
|---|---|
| gold | `#C9A227` |
| carbon | `#0D0D0D` |
| panel | `#1A1A1A` |
| paper / cream | `#F5F0E6` |
