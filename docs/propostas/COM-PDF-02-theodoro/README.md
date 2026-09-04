# COM-PDF-02 — proposta Theodoro / Variant AIW3138

**Status:** rascunho interno, **não publicado**. Não enviar ao cliente. Não implantar site. Não postar em canal nenhum.

Primeira passagem **só texto**. Fotos **não** estão prontas: a pasta Drive `00_Antes` está vazia; IDs de arquivo anteriores eram stubs. Esta pasta **não** baixa, inventa nem embute foto.

O embed fotográfico entra em **PR de follow-up**, depois que arquivos reais **> 100 KB** forem dropados em `00_Antes`. Upload: seguir [`docs/drive-binary-upload.md`](../../drive-binary-upload.md) (proibido MCP `create_file`).

## O que é

Proposta comercial HTML + CSS de impressão (A4) da **Heros Custom** (oficina) para o interlocutor **Theodoro**, veículo **Variant Type 3, 1975, placa AIW3138**.

Conteúdo comercial travado no brief de Comunicação (Portal / OS):

| Pacote | Nome | Mão de obra |
|---|---|---|
| **A** | Elétrica corretiva pontual | **R$ 1.850** |
| **B** | Elétrica completa Padrão Heros | **R$ 4.200** |

Peças à parte, com nota no CNPJ FSE. Cobrança = **pacote**, não hora. A tabela F0–F8 (~28–47 h) é **previsão de bancada** do Pacote B.

## Refs internas (não vão no PDF / HTML da proposta)

Estes códigos ficam **só neste README**. Não colar URL viva de Notion nem CPF no artefato:

- OS-34
- PD-4
- HC-2026-025
- Laudo elétrico #21 (checklist genérico no HTML, sem medição inventada)

## Como regenerar localmente

Fonte: `index.html` + `print.css`. Não há WeasyPrint/reportlab nas deps do Hub.

### 1. Ver no navegador

```bash
cd docs/propostas/COM-PDF-02-theodoro
python3 -m http.server 4176 --bind 127.0.0.1
```

Abrir http://127.0.0.1:4176/ — **não** é deploy.

### 2. Salvar PDF (Chrome / Chromium)

Pelo diálogo: Arquivo → Imprimir → Destino **Salvar como PDF** → A4 → fundos de gráfico ligados.

Pela linha de comando (mesmo Chrome do ambiente):

```bash
./emitir-pdf.sh
```

Saída: `COM-PDF-02-theodoro-texto.pdf` (só texto; slots fotográficos = AUSENTE). Um snapshot desse PDF pode estar commitado nesta pasta; regenerar localmente o substitui.

Requisitos: `google-chrome` ou `chromium` no PATH. Sem foto, sem rede obrigatória (Montserrat/Inter caem no fallback se o Google Fonts não carregar).

## Fotos — hold

Slots no HTML (todos **AUSENTE / aguardando drop manual > 100 KB**):

1. Impressão geral (print)
2. Faróis
3. Chicote
4. Luz de placa
5. Lanternas
6. Farol E
7. Partida
8. Caixa de fusíveis (**especialmente vazia**)

Não usar stock, render, placeholder que pareça o carro, nem ID stub antigo.

## Regras duras deste artefato

- Sem CPF
- Sem Type 1 / Mestra Fusca / diagrama N0
- Sem URL viva de Notion
- Sem Instagram
- Sem n8n
- Sem foto embutida (`<img>` proibido nesta passagem)
- Não enviar ao cliente até OK do Ricardo **e** fotos reais em `00_Antes`

## Marca

Heros Custom · Gold v1.1 (COM-ALIGN-01) · Montserrat (títulos) + Inter (corpo).

| Token | HEX |
|---|---|
| gold | `#C9A227` |
| carbon | `#0D0D0D` |
| panel | `#1A1A1A` |
| paper / cream | `#F5F0E6` |

Fatura / CNPJ: Fidalgo Soluções Elétricas LTDA **31.402.321/0001-46**. WhatsApp oficina **(41) 99187-8091**.
