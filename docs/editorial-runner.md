# Mesa editorial — runner (Heros Custom)

**Status:** código no repo, dry-run por padrão. **Aprovar nunca publica. Publicado é só do Ricardo. Não há escrita n8n / IG / PDF / site.**

Sibling do [Painel Founder](../README.md#painel-founder-como-rodar). Mesmo espírito: pulso + ações de mesa, Notion como SSOT, escrita atrás de `NOTION_TOKEN` + `CONFIRM=1`. **Não** é um segundo SSOT, **não** é um 7º bot / AGT-09 e **não** existe um segundo runner (`editorial/` foi descartado).

Módulo único: `dashboard/editorial_runner.py` + `dashboard/editorial_status.py` + `dashboard/editorial_canon.py`.

---

## O que é

Mesa (não empresa nova, não quarta porta pública) com dois braços:

| Braço | Entrega | Agente |
|---|---|---|
| **Editora** | Livro, almanaque, módulo, ficha, clube | Acervo |
| **Produtora** | Reels, carrossel, roteiro, prova 4:3 | Comunicação |

Marca no ar: **Heros Custom**. Chip Grupo Fidalgo só no rodapé.

SSOT da fila: [Fila Editorial — Editora × Produtora](https://app.notion.com/p/8af724e1f3964864a1e2e9840c741047)  
Mesa: [Mesa editorial · Editora × Produtora (Heros)](https://app.notion.com/p/3c97d36bae6481ceb08df218c3d02ba8)

IDs (sem secrets) vivem em `config/notion_ids.json` → `databases.fila_editorial` (`write=false`, `runner_only=true`). Não inventar outra lista.

---

## Dry-run (padrão)

Sem flags, ou com `--dry-run`, o CLI lista a fila e o PATCH **planejado**. Não escreve no Notion. Sem `NOTION_TOKEN` usa `dashboard/fixtures/sample_fila_editorial.json` (EDI-1 kit Datar, EDI-2 reel Anchieta).

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha NOTION_TOKEN se for ler live; não commite .env

# Pulso + transições planejadas (padrão)
python -m dashboard.editorial_runner
python -m dashboard.editorial_runner --dry-run

# Ainda dry-run: imprime Status=Aprovado. Não grava, não publica.
python -m dashboard.editorial_runner --approve EDI-1
python -m dashboard.editorial_runner --refuse EDI-2 --reason "mito 12V 1967"

# Status atual se o card não estiver na fila carregada
python -m dashboard.editorial_runner --approve <PAGE_ID> --status "Aguardando OK"
```

Flags:

| Flag | Efeito |
|---|---|
| `--dry-run` | Lista fila + PATCH planejado (também o padrão sem ação) |
| `--approve PAGE_ID` | Planeja Rascunho/Aguardando OK → **Aprovado**. Dry-run sem `CONFIRM=1` |
| `--refuse PAGE_ID` | Planeja → **Recusado**. Exige `--reason` ≥ 8 caracteres |
| `--reason TEXT` | Observação (aprovar) ou motivo (recusar) |
| `--status STATUS` | Status atual se o card não estiver na fila |

Escrita no Notion **só** se:

1. `NOTION_TOKEN` estiver definido, **e**
2. `CONFIRM=1`

```bash
CONFIRM=1 python -m dashboard.editorial_runner --approve EDI-1
```

Sem os dois, o CLI imprime o PATCH e para. Não há checkbox de UI neste módulo (é CLI, não o Flask do Founder). Mesmo com `CONFIRM=1` o payload só leva `Status=Aprovado` (e talvez `Observações`). **Canal não muda. Publicado não é definido. n8n não dispara.**

---

## Contrato de status

Schema vivo (não inventar opção):

`Rascunho` → `Aguardando OK` → `Aprovado` → `Publicado`  
`Recusado` encerra.

| Ação | De | Para | Efeito colateral |
|---|---|---|---|
| **Aprovar** | Rascunho ou Aguardando OK | **Aprovado** | Nenhum. Sem IG, sem site, sem n8n, sem webhook, sem PDF. Não marca Automação executada. Não muda Canal. |
| **Recusar** | Rascunho, Aguardando OK ou Aprovado | **Recusado** | Só Observações `[Recusa editorial]`. Exige motivo ≥ 8 caracteres. |
| **Publicar** | — | — | **Não existe.** O runner recusa a ação. |

**`Publicado` é estado humano / Ricardo.** Este runner nunca grava `Publicado`. Card já publicado não é mexido.

Canal padrão: **Não publicar**. Aprovar um card cujo Canal seja IG **ainda assim não posta** — Aprovar só muda Status para Aprovado.

Não há ações `adiar`, `novo` ou `pulse` neste runner. Não há pacote `editorial/`.

---

## Canon (bloqueia Aprovar)

`dashboard/editorial_canon.py` varre Peça / Métrica / Observações / Próxima ação. Mito ou figura inventada **bloqueia Aprovar** (inclusive no dry-run: o card vai para `canon_blocked`, não para `planned`). Figura fora da lista canônica é recusada, não aceita em silêncio.

| Proibido | Canônico |
|---|---|
| 12 V = **1967** | 12 V no Brasil = **1968** |
| 12 V implica alternador | 12 V **não** implica alternador |
| fim BR = **2003** | fim de linha BR = **1996** (2003 é México) |
| Anchieta com ano/data trocada | nacional **03/01/1959**; planta **18/11/1959** |
| Volume inflado (ex.: “2 milhões”) | Só os já cravados: Ipiranga CKD **2.268** Sedan; Itamar **47.700** |
| OS viva / CPF | Não entram em peça editorial |
| NAP EF/FSE, 557 como endereço público | NAP pública **439**; **557** é clube |

---

## O que este runner não faz

- **Aprovar nunca publica.**
- **Publicado é só do Ricardo.**
- Não posta no Instagram (nem Graph API, nem n8n, nem webhook).
- Não escreve PDF, site ou Clube. Não toca `sites/`.
- Não dispara n8n em nenhuma ação.
- Não cria AGT-09 nem 7º bot Grok.
- Não escreve Fila Founder, OS, CRM, Clientes ou Financeiro.
- Não mistura CNPJ/caixa Heros vs FSE.

O Painel Founder (`python -m dashboard.app`) continua dono da Central de Comando. A mesa editorial é **irmã**, não substituta.

---

## Testes

```bash
CONFIRM=0 python -m pytest tests/test_editorial_runner.py tests/test_editorial_canon.py -q
```

A CI do painel (`founder_panel_tests.yml`) roda `tests/` inteiro com `CONFIRM=0`.
