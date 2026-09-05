# COM-PDF-APR-N0 — pacote Aprendiz (N0 Type 1)

**Status:** rascunho interno, **não publicado**. Sem site até OK Founder. Não implantar. Não enviar a aluno como curso no ar.

**Aprendiz testa como aluno** — lê Camada A, responde A1–A6, aplica o checklist 1–7. Não trata este PDF como publicação.

Duas camadas no mesmo artefato:

| Camada | O que é | Neste PDF |
|---|---|---|
| **A · Ensino Type 1** | Critério N0 (6 aulas, A1–A6, §10, Quiz D1, checklist, E1–E3) | Completa (texto) |
| **B · Execução** | Só com Passaporte tipado (ano + tensão + foto caixa + foto gerador) | **Esqueleto vazio** — sem carro |

## O que é

Curso inicial **elétrica simples**, padrão Heros, plataforma **Type 1**. Não é M1 chicote. Não são os 9 procedimentos de bancada. **Hércules** = método de oficina, não o nome do curso.

Canon compilado da ementa N0 + briefing Aprendiz (04/09/2026):

- 12 V BR = **1968**
- 12 V ≠ alternador
- Fim BR = **1996** (2003 = México)
- 1º nacional **03/01/1959**
- Planta Anchieta **18/11/1959**

CTA no miolo: **Próximo: M1 chicote — ou agendar diagnóstico**. Sem NAP, sem WhatsApp, sem telefone. Contato = página de vendas depois, não neste PDF.

## Refs internas (não vão no HTML / PDF)

Estes nomes ficam **só neste README**. Não colar URL viva de Notion nem CPF no artefato:

- Ementa N0 — Curso inicial elétrica simples
- Briefing PDF Aprendiz · Camada A + B
- Quiz D1 — 10Q + gabarito copiados da página editorial (sem inventar)
- D1 Pista C (fonte aula 2; Cap. 1 §5 = rascunho, não pré-requisito)
- Ponte 01/09 (E1–E3)
- Chicote U2 / bitolas = **só Camada B / M1**, não N0

## Como regenerar localmente

Fonte: `index.html` + `print.css`. Não há WeasyPrint/reportlab nas deps do Hub.

### 1. Ver no navegador

```bash
cd docs/propostas/COM-PDF-APR-N0
python3 -m http.server 4177 --bind 127.0.0.1
```

Abrir http://127.0.0.1:4177/ — **não** é deploy.

### 2. Salvar PDF (Chrome / Chromium)

Pelo diálogo: Arquivo → Imprimir → Destino **Salvar como PDF** → A4 → fundos de gráfico ligados.

Pela linha de comando:

```bash
./emitir-pdf.sh
```

Saída: `COM-PDF-APR-N0-aprendiz.pdf`. Um snapshot pode estar commitado nesta pasta; regenerar localmente o substitui.

Requisitos: `google-chrome` ou `chromium` no PATH. Sem foto, sem rede obrigatória (Montserrat/Inter caem no fallback se o Google Fonts não carregar).

## P1 (não agora)

Hold de diagramação — **não** neste PDF:

- 1 aula / folha
- Quiz D1 em folhas próprias (○ vazia no miolo já está)

## Fotos-modelo — AUSENTE

Slots da Camada A (`caixa 8 pólos` · `caixa 12 pólos` · `dínamo vs alternador`) e campos da Camada B = **AUSENTE**. Hold Founder/Ops — sem foto inventada, sem stock, sem `<img>`.

## Regras duras deste artefato

- Sem CPF
- Sem OS viva / número de OS viva
- Sem placa de cliente
- Sem preço / SKU inventado
- Type 3 = outro módulo; não usar como material de ensino deste N0
- Sem PDF 67–81 genérico
- Sem URL viva de Notion
- Sem Instagram
- Sem n8n
- Sem foto embutida (`<img>` proibido)
- Sem site até OK Founder
- Camada B vazia até Passaporte tipado

## Marca

Heros Custom · Gold v1.1 (COM-ALIGN-01) · Montserrat (títulos) + Inter (corpo).

| Token | HEX |
|---|---|
| gold | `#C9A227` |
| carbon | `#0D0D0D` |
| panel | `#1A1A1A` |
| paper / cream | `#F5F0E6` |

Marca oficina: Heros Custom. NAP / WhatsApp de contato **não** vão no HTML/PDF até OK COM/Founder.
