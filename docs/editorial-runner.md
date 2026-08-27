# Mesa editorial — runner (Heros Custom)

**Status:** código no repo, dry-run por padrão. **Não publica. Não posta no Instagram. Nada no ar.** Merge fica a cargo do Ricardo.

Sibling do [Painel Founder](../README.md#painel-founder-como-rodar). Mesmo espírito: pulso + ações de mesa, Notion como SSOT, escrita atrás de `NOTION_TOKEN` + `CONFIRM=1`. **Não** é um segundo SSOT e **não** é um 7º bot / AGT-09.

---

## O que é

Mesa (não empresa nova, não quarta porta pública) com dois braços:

| Braço | Entrega | Agente |
|---|---|---|
| **Editora** | Livro, almanaque, módulo, ficha, clube | Acervo |
| **Produtora** | Reels, carrossel, roteiro, prova 4:3 | Comunicação |

Marca no ar: **Heros Custom**. Chip Grupo Fidalgo só no rodapé. Staff cheio (6). Sem bot novo.

SSOT da fila: [Fila Editorial — Editora × Produtora](https://app.notion.com/p/8af724e1f3964864a1e2e9840c741047)  
Mesa: [Mesa editorial · Editora × Produtora (Heros)](https://app.notion.com/p/3c97d36bae6481ceb08df218c3d02ba8)

IDs (sem secrets) vivem em `config/notion_ids.json` → `databases.fila_editorial`. Não inventar outra lista.

---

## Dry-run (padrão)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha NOTION_TOKEN se for ler live; não commite .env

# Pulso (fixture se não houver token)
python -m editorial
python -m editorial pulse

# Ações: imprimem o payload Notion e NÃO escrevem
python -m editorial aprovar <PAGE_ID> --status "Aguardando OK"
python -m editorial recusar <PAGE_ID> --status "Rascunho" --reason "mito 12V 1967"
python -m editorial adiar <PAGE_ID> --status "Aguardando OK" --reason "esperar grid"
python -m editorial novo --peca "EDI · Ficha hold" --braco Editora --formato Ficha
```

Escrita no Notion **só** se:

1. `NOTION_TOKEN` estiver definido, **e**
2. `CONFIRM=1`

```bash
CONFIRM=1 python -m editorial aprovar <PAGE_ID>
```

Sem os dois, o CLI imprime o PATCH e para. Não há checkbox de UI neste módulo (é CLI, não o Flask do Founder).

---

## Contrato de status

Schema vivo (não inventar opção):

`Rascunho` → `Aguardando OK` → `Aprovado` → `Publicado`  
`Recusado` encerra. **Não existe Adiado** nesta database.

| Ação | De | Para | Efeito colateral |
|---|---|---|---|
| **Aprovar** | Rascunho ou Aguardando OK | **Aprovado** | Nenhum. Sem IG, sem site, sem n8n, sem webhook. Não marca Automação executada. Não muda Canal. |
| **Recusar** | Rascunho, Aguardando OK ou Aprovado | **Recusado** | Só Observações `[Recusa Mesa]`. Exige motivo ≥ 8 caracteres. |
| **Adiar** | Rascunho, Aguardando OK ou Aprovado | **Rascunho** | Nota em Observações / Próxima ação. Não inventa status Adiado. |
| **novo** | — | **Rascunho** | Canal **sempre** `Não publicar`. Automação executada = false. |
| **Publicar** | — | — | **Não existe.** O runner recusa a ação. |

**`Publicado` é status do Founder.** Este runner nunca grava `Publicado`. Card já publicado não é mexido.

Canal padrão de card novo: **Não publicar**. Aprovar um card cujo Canal seja IG **ainda assim não posta** — Aprovar só muda Status para Aprovado.

---

## Pulso

Read-only:

- Contagens por **Status**
- Contagens por **Braço**
- Próximo item em **Aguardando OK** (menor Nº EDI- primeiro)

Sem token, usa `editorial/fixtures/sample_fila.json` (espelho dos cards SIM da mesa + um Aguardando OK de demonstração).

---

## Canon (bloqueia Aprovar / novo)

Qualquer card cuja **Métrica** (ou Peça / Observações) invente volume ou repita mito é recusado:

| Proibido | Canônico |
|---|---|
| 12 V = **1967** | 12 V = **1968** |
| fim BR = **2003** | fim BR = **1996** (México = 2003) |
| Volume inflado | Só os já cravados: CKD Ipiranga **2.268**, Itamar **47.700** |
| OS viva / CPF | Não entram em peça editorial |
| NAP EF/FSE, 557 como endereço público | NAP pública **439**; **557** é clube |

---

## O que este runner não faz

- Não postar no Instagram (nem Graph API, nem n8n, nem webhook).
- Não publicar no site / PDF / Clube.
- Não criar AGT-09 nem 7º bot Grok.
- Não escrever OS Status Entregue, CRM, Financeiro ou Fila Founder.
- Não misturar CNPJ/caixa Heros vs FSE.

O Painel Founder (`python -m dashboard.app`) continua dono da Central de Comando. A mesa editorial é **irmã**, não substituta.

---

## Testes

```bash
CONFIRM=0 python -m pytest tests/test_editorial_status.py tests/test_editorial_canon.py tests/test_editorial_guard.py tests/test_editorial_cli.py -q
```

A CI do painel (`founder_panel_tests.yml`) também roda `tests/` inteiro, inclusive estes, com `CONFIRM=0`.
