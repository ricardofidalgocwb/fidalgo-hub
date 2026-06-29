# Fidalgo Hub - Sistema de Governança Automatizada

## 📊 Visão Geral

O **Fidalgo Hub** é um sistema integrado de governança financeira e familiar que automatiza validações, sincroniza dados com Notion e fornece relatórios inteligentes para tomada de decisão.

**Status:** ✅ Production Ready v3 Final

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
├── .github/
│   └── workflows/
│       └── weekly_metrics_validation.yml    # ✅ Workflow automático
├── validate_and_sync_notion_v2_final.py     # ✅ Script principal
├── template_dados_completo.json              # ✅ Template de dados
├── README.md                                 # 📖 Você está aqui
├── SETUP_GUIDE.md                            # 📖 Guia de configuração
├── WORKFLOW_DOCUMENTATION.md                 # 📖 Docs técnicas
└── validation_report_*.json                  # 📊 Artefatos (gerados)
    validation_report_*.md                   # 📊 Artefatos (gerados)
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
