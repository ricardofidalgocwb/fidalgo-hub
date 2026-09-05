# COM-PDF-CAP2-motor — Cap. 2 Anatomia do motor boxer a ar (Type 1)

**Status:** rascunho interno 0.2, **não publicado**. Sem site até OK Founder. Não implantar. Não enviar como curso no ar. Pacote **separado** do COM-PDF-APR-N0 / PR#15.

**Aprendiz testa como aluno** — lê §§1–5, marca o checklist 1–8 ☐, responde o quiz «nomeie a peça». Não trata este PDF como publicação.

| Bloco | O que é | Neste PDF |
|---|---|---|
| **Capa** | Type 1 · anatomia motor refrigerado a ar · unpublished | Completa |
| **Miolo Cap.2** | Conceito · fluxo ar/óleo · tinware · spec códigos · ponte bancada | Completa (texto Acervo) |
| **Bridge Aprendiz** | Checklist peças 1–8 + ☐ + selo domínio | Completa |
| **Quiz** | «Nomeie a peça» 10Q · gabarito **só no fim** | Completa |
| **Ponte N0** | Tensão + caixa + gerador = outro PDF | Só ponte — não miolo |

## O que é

Capítulo 2 do livro Type 1 (refrigerado a ar): **anatomia do motor boxer a ar**. Padrão Heros. Não é N0 elétrica. Não é M0 Caps 1+3+4 no mesmo arquivo. Não são os 9 procedimentos de bancada.

Cânon motor (Acervo, rascunho 0.2):

- Boxer a ar · comando no bloco · motor atrás
- Ordem de ignição clássica **1-4-3-2**
- Códigos B / BF / BH / BB / BD · Itamar 1600 (1993–96)
- Elétrica = ponte N0 / Cap.14 (item 9) — **não** miolo
- Sem cv neste capítulo. Folga / torque ficam na tabela do Acervo (não duplicar)

Selo domínio: **8 ☐** + não misturou N0 no miolo motor.

## Refs internas (não vão no HTML / PDF)

Estes nomes ficam **só neste README**. Não colar URL viva de Notion nem CPF no artefato:

- Cap. 2 — Anatomia do motor boxer a ar (Mestra, rascunho 0.2)
- EDI- Briefing PDF Cap.2 anatomia + quiz «nomeie a peça»
- EDI- Cap.2 + quiz «nomeie a peça» · PDF unpublished
- Linha do Tempo + Códigos Motor (spec B/BF/BH/BB/BD)
- Cap. 14 / N0 = elétrica (outro PDF)
- M0 Caps 1+3+4 = história / era (outro arquivo)

## Como regenerar localmente

Fonte: `index.html` + `print.css`. Não há WeasyPrint/reportlab nas deps do Hub.

### 1. Ver no navegador

```bash
cd docs/propostas/COM-PDF-CAP2-motor
python3 -m http.server 4178 --bind 127.0.0.1
```

Abrir http://127.0.0.1:4178/ — **não** é deploy.

### 2. Salvar PDF (Chrome / Chromium)

Pelo diálogo: Arquivo → Imprimir → Destino **Salvar como PDF** → A4 → fundos de gráfico ligados.

Pela linha de comando:

```bash
./emitir-pdf.sh
```

Saída: `COM-PDF-CAP2-motor.pdf`. Um snapshot pode estar commitado nesta pasta; regenerar localmente o substitui.

Requisitos: `google-chrome` ou `chromium` no PATH. A tipada Commons está em `assets/` (local; sem rede). Montserrat/Inter caem no fallback se o Google Fonts não carregar.

## Fotos-modelo — tinware Commons (unpublished)

**Status:** rascunho interno, **não publicado**. Sem site até OK Founder.

Slot liberado Ops 05/09 (Commons SRC, ≥100 KB, Type 1, sem stock/IA):

| Slot | Arquivo | Drive ID | Bytes |
|---|---|---|---|
| Tinware completo (didático) | `assets/Cap2_engineBay_SRC-commons.jpg` | `1eQ_Oev74l_kmD_JLftGdVSBc9uFsboE2` | 193513 |

[Drive](https://drive.google.com/file/d/1eQ_Oev74l_kmD_JLftGdVSBc9uFsboE2/view) · cite no HTML: Wikimedia Commons (SRC-commons).

**AUSENTE:** prefixo bloco · ventoinha/correia · tinware incompleto.

**Não embutir:** `Cap2_engine1962` (DUP de N0 A.8) · `M6_T_engineBayTin` (DUP deste bay).

## Regras duras deste artefato

- Sem CPF / OS viva / placa de cliente
- Sem site até OK Founder
- Sem URL viva de Notion
- Sem Instagram
- Sem n8n
- Sem foto de cliente / stock / IA; só a tipada Commons do tinware didático
- Sem cv / torque / folga / pistão inventado
- Sem misturar N0 no miolo motor (item 9 = só ponte)
- Type 3 = outro módulo
- BV / Brasília / SP2 (BL 1678) = fora (não são Type 1 Fusca)
- Sem Hércules-curso (método de box ≠ nome deste capítulo)
- Quiz: sem marca de acerto nas opções; gabarito só no fim
- Pacote separado do COM-PDF-APR-N0

## Marca

Heros Custom · Gold v1.1 (COM-ALIGN-01) · Montserrat (títulos) + Inter (corpo).

| Token | HEX |
|---|---|
| gold | `#C9A227` |
| carbon | `#0D0D0D` |
| panel | `#1A1A1A` |
| paper / cream | `#F5F0E6` |
