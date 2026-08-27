# Fidalgo Hub — Multi-Asset Control Dashboard

Painel operacional interno da **Heros Custom** (nunca Eros / Eletric). Notion é a fonte única de verdade. Founder: Ricardo Rodriguez Fidalgo.

**Regra de ouro:** Grok Bot roteia → card na Fila Founder → Founder dá OK (**Aprovar**) → só então **Avançar** pode executar. O painel **não dispara n8n em Aprovar**.

---

## Painel Founder (como rodar)

Pulso read-only (contagens por status + próximo item L0) e botões **Aprovar / Avançar / Recusar / Adiar** que só PATCHeiam propriedades do card na Fila Founder.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha NOTION_TOKEN; não commite .env

# Dry-run (padrão): imprime o payload Notion, não escreve
python -m dashboard.app
# Abra http://127.0.0.1:5050

# Testes da máquina de status + guarda n8n
python -m pytest tests/ -q
```

Escrita no Notion só acontece se:

1. `NOTION_TOKEN` estiver definido, **e**
2. `CONFIRM=1` **ou** a UI marcar “Confirmar escrita no Notion”.

```bash
# CLI/servidor com escrita liberada (ainda exige confirmação na UI se você quiser o checkbox)
CONFIRM=1 python -m dashboard.app
```

n8n permanece **desligado**. Para (opcionalmente) avisar o motor só em **Avançar**:

```
N8N_AVANCAR_ENABLED=1
N8N_AVANCAR_WEBHOOK=https://seu-n8n/webhook/...
```

IDs canônicos (sem secrets) estão em `config/notion_ids.json`, espelhados do Hub Claude Code e da Fila Founder ao vivo. CRM SSOT = `6157d36b…`. Não usar Leads arquivado `43b3f514`. Este painel **não** escreve OS Status Entregue nem mistura CNPJ/caixa Heros vs FSE.

Pipeline (português, schema Notion): Aguardando OK → Aprovado → Em Execução → Concluído; Recusar → Rejeitado; Adiar → Adiado.

---

## Runner editorial (Editora × Produtora)

Fila SSOT: [Fila Editorial — Editora × Produtora](https://app.notion.com/p/8af724e1f3964864a1e2e9840c741047) (`8af724e1…`, ds `13be9ea3…`). **Aprovar ≠ publicar.** O runner não define `Publicado` (estado só do Ricardo), não muda Canal (`Não publicar` permanece), não dispara n8n, não posta IG, não gera PDF e não toca os sites.

```bash
# Dry-run (padrão): lista a fila e o PATCH planejado. Sem token usa fixtures EDI-1 / EDI-2.
python -m dashboard.editorial_runner --dry-run

# Ainda dry-run: imprime Status=Aprovado. Só grava com NOTION_TOKEN + CONFIRM=1.
python -m dashboard.editorial_runner --approve EDI-1
CONFIRM=1 python -m dashboard.editorial_runner --approve EDI-1
```

`config/notion_ids.json` marca `fila_editorial.write=false` (runner-only). Mesmo com `CONFIRM=1` o payload só leva `Status=Aprovado` (e talvez `Observações`). Peças ao vivo na fila (não inventadas): **EDI-1** kit Datar (M0 D1) e **EDI-2** reel Anchieta 1959, ambas Canal=Não publicar / Status=Rascunho.

Sincronismo se a peça citar data: 12 V BR = **1968**; fim BR = **1996**. Sem NAP de Eletro Fidalgo.

---

# Governança automatizada (workflow semanal)

O **Fidalgo Hub** também valida dados de governança financeira e familiar, sincroniza com Notion e gera relatórios.

**Status workflow semanal:** Production Ready v3 Final

---

## 🎯 Funcionalidades Principais

### ✅ Validação Automática Semanal
- Executa todo **domingo às 22:00 UTC** (19:00 BRT)
- Valida integridade dos dados de governança
- Gera relatórios em **JSON** e **Markdown**
- Histórico armazenado por **30 dias**

### 📧 Notificações Inteligentes
- **⚠️ WARNING**: Alertas que requerem atenção
- **❌ FAIL**: Erros críticos imediatos
- **✅ SUCCESS**: Silencioso (esperado)

### 🔄 Sincronização Notion
- Atualiza Notion Database com status
- Registra histórico completo
- Rastreia mudanças e tendências

### 📈 Relatórios Estruturados
- JSON para integração com sistemas
- Markdown legível para humanos
- Métricas resumidas e detalhadas

---

## 📁 Estrutura do Repositório

```
fidalgo-hub/
├── config/notion_ids.json                    # IDs Notion SSOT (sem secrets)
├── dashboard/                                # Painel Founder + runner editorial
├── tests/                                    # Máquina de status + guarda n8n + editorial
├── .github/workflows/
│   ├── weekly_metrics_validation.yml
│   └── founder_panel_tests.yml
├── validate_and_sync_notion_v2_final.py
├── template_dados_completo.json
└── README.md
```

---

## 🚀 Quick Start (5 Minutos)

### 1️⃣ Verificar Arquivos
```bash
# Confirme que os arquivos necessários existem no root
ls validate_and_sync_notion_v2_final.py template_dados_completo.json .github/workflows/weekly_metrics_validation.yml
```

### 2️⃣ Configurar 5 Secrets
Acesse: `Settings` → `Secrets and variables` → `Actions`

Crie estes secrets:
```
NOTION_TOKEN              = seu token do Notion
NOTION_DATABASE_ID        = id da database
GMAIL_USER                = seu-email@gmail.com
GMAIL_APP_PASSWORD        = senha app do Gmail (16 chars com espaço)
RECIPIENT_EMAIL           = destinatario@email.com
```

👉 [Instruções Detalhadas: SETUP_GUIDE.md](./SETUP_GUIDE.md)

### 3️⃣ Testar Manualmente
1. Vá em: `Actions` → `Fidalgo Hub - Validação Semanal`
2. Clique: `Run workflow` (verde)
3. Escolha: `main`
4. Clique: `Run workflow`

**Espere ~3 minutos** e verifique:
- ✅ Logs: `Actions` → clique na execução
- ✅ Email: Procure notificação em sua caixa
- ✅ Artefatos: Download dos relatórios

### 4️⃣ Próxima Execução
- **Automática:** Próximo domingo 22:00 UTC
- **Manual:** A qualquer momento via `Run workflow`

---

## 📊 Dados que Validamos

O workflow valida 5 categorias de dados:

### 1. Pessoa Física (PF)
```json
{
  "renda_mensal_pf": 8000,
  "despesas_mensais_pf": 5000,
  "caixa_aplicacoes_total": 55000,
  "fluxo_real_mensal": 10500,
  "fluxo_projetado_mensal": 10000
}
```

### 2. FSE (Fundo de Separação Familiar)
```json
{
  "distribuicoes_mensais_fse": 8000,
  "saldo_dividas_total": 0
}
```

### 3. Eletroposto (Investimento)
```json
{
  "eletroposto_capex_total": 1500000,
  "eletroposto_receitas_anuais_proj": 400000,
  "eletroposto_custos_anuais_proj": 150000
}
```

### 4. Imóveis
```json
{
  "imoveis_count": 4,
  "casa_quitada": true,
  "valor_mercado_estimado_imoveis": 2500000
}
```

### 5. Planejamento Sucessório
```json
{
  "ativos_transferidos_pct": 20,
  "itcmd_estimado_economia": 120000,
  "risco_score_macro": 3.0
}
```

---

## ⏰ Schedule e Timezone

| Aspecto | Valor |
|--------|-------|
| **Frequência** | Semanal |
| **Dia** | Domingo |
| **Hora UTC** | 22:00 |
| **Hora BRT** | 19:00 (mesmo domingo) |
| **Próxima** | Próximo domingo 22:00 UTC |

---

## 🔐 Segurança

### Proteção de Secrets
✅ Não aparecem em logs  
✅ Não são commitados  
✅ Encriptados pelo GitHub  
✅ Masked em outputs  

### Boas Práticas
- ✅ Use secrets para dados sensíveis
- ✅ Revise logs regularmente
- ✅ Monitore emails de notificação
- ✅ Mantenha database Notion sincronizada

---

## 📧 Notificações por Email

### Quando Você Recebe Email?

**⚠️ WARNING**
- Alertas que requerem atenção
- Assunto: `⚠️ Fidalgo Hub - Validação Semanal: WARNING`
- Inclui: Link para workflow, logs, recomendações

**❌ FAIL**
- Erros críticos
- Assunto: `❌ Fidalgo Hub - Validação Semanal: FAIL`
- Urgente: Requer ação imediata

**✅ SUCCESS**
- Sem notificação (esperado)
- Tudo funcionando normalmente
- Você pode consultar artefatos manualmente

---

## 🔧 Workflow v3 Final - Etapas

### Visão Geral do Fluxo

```
Agendamento (Cron)
        ↓
    Checkout
        ↓
    Debug: Arquivos
        ↓
    Setup Python 3.11
        ↓
    Instalar Dependências
        ↓
    Debug: Secrets
        ↓
    Executar Script Python
    ├─ Validar dados
    ├─ Sincronizar Notion
    ├─ Gerar relatórios
    └─ Enviar emails
        ↓
    Upload Artefatos
        ↓
    Status: SUCCESS / WARNING / FAIL
```

### Steps Detalhados

| # | Step | Função | Output |
|---|------|--------|--------|
| 1 | **Checkout** | Baixa código | ✅ Repo clonado |
| 2 | **Debug: Arquivos** | Lista estrutura | 📁 Arquivos encontrados |
| 3 | **Python 3.11** | Setup ambiente | 🐍 Python configurado |
| 4 | **Instalar Deps** | `notion-client`, `python-dotenv` | 📦 Deps instaladas |
| 5 | **Debug: Secrets** | Valida configuração | 🔑 Secrets OK |
| 6 | **Validação** | Roda script Python | 📊 Validação completa |
| 7 | **Upload** | Salva relatórios | 📄 Artefatos salvos |

---

## 📈 Monitoramento

### Dashboard GitHub Actions
`Actions` → `Fidalgo Hub - Validação Semanal`

**O que você vê:**
- ✅ Histórico de todas as execuções
- ✅ Status (SUCCESS/WARNING/FAIL)
- ✅ Tempo de execução
- ✅ Logs detalhados por step

### Relatórios Semanais
Baixe artefatos em `weekly-validation-reports`:
- `validation_report_YYYYMMDD_HHMMSS.json`
- `validation_report_YYYYMMDD_HHMMSS.md`

### Alertas por Email
Receba notificações automáticas:
- WARNING: Alertas
- FAIL: Erros críticos

---

## ❓ FAQ Rápido

### P: Posso executar manualmente?
**R:** Sim! `Actions` → `Run workflow` → `main` → `Run workflow`

### P: Em que linguagem é escrito?
**R:** Python 3.11. Bibliotecas: `notion-client`, `python-dotenv`

### P: Onde baixo os relatórios?
**R:** `Actions` → execução → `Artifacts` → `weekly-validation-reports`

### P: Posso mudar dia/hora?
**R:** Sim, edite `.github/workflows/weekly_metrics_validation.yml` e altere o `cron`

### P: O que se não configurar os secrets?
**R:** Script executa mas mostra erros, sem sincronização Notion/email

### P: Quanto tempo demora?
**R:** ~3-4 minutos (depende do script Python)

### P: Quanto tempo guardama os relatórios?
**R:** 30 dias como artefatos do GitHub

---

## 🐛 Troubleshooting Rápido

### Erro: Script não encontrado
```bash
git add validate_and_sync_notion_v2_final.py
git commit -m "Add validation script"
git push
```

### Erro: Email não enviado
1. Verifique `GMAIL_APP_PASSWORD` (use app password, não senha da conta)
2. Valide `RECIPIENT_EMAIL` (não pode estar vazio)
3. Confirme Gmail 2FA está ativado

### Erro: Notion não sincronizando
1. Verifique `NOTION_TOKEN`
2. Verifique `NOTION_DATABASE_ID`
3. Confirme que database existe

👉 [Troubleshooting Completo: SETUP_GUIDE.md](./SETUP_GUIDE.md#-troubleshooting)

---

## 📚 Documentação Detalhada

Para mais informações, consulte:

| Documento | Conteúdo |
|-----------|----------|
| [SETUP_GUIDE.md](./SETUP_GUIDE.md) | Passo a passo de configuração + troubleshooting |
| [WORKFLOW_DOCUMENTATION.md](./WORKFLOW_DOCUMENTATION.md) | Documentação técnica completa |
| [GitHub Actions Docs](https://docs.github.com/en/actions) | Documentação oficial GitHub |
| [Notion API](https://developers.notion.com) | API do Notion |

---

## 🎯 Próximos Passos

1. ✅ Leia este README
2. ✅ Siga [SETUP_GUIDE.md](./SETUP_GUIDE.md)
3. ✅ Configure 5 secrets
4. ✅ Execute manualmente para testar
5. ✅ Revise relatórios e logs
6. ✅ Monitore próxima execução automática

---

## 📊 Versão e Status

| Aspecto | Valor |
|--------|-------|
| **Versão** | v3 Final |
| **Status** | ✅ Production Ready |
| **Data** | 2026-06-29 |
| **Próxima Execução** | Próximo domingo 22:00 UTC |
| **Suporte** | Veja [SETUP_GUIDE.md](./SETUP_GUIDE.md) |

---

## 🙌 Créditos

**Sistema de Governança Automatizada**  
Fidalgo Hub v3 Final

Desenvolvido para automatizar validações de governança financeira e familiar com máxima confiabilidade e rastreabilidade.

---

**Pronto para começar?** 👉 [SETUP_GUIDE.md](./SETUP_GUIDE.md)

Dúvidas? 👉 [WORKFLOW_DOCUMENTATION.md](./WORKFLOW_DOCUMENTATION.md)
