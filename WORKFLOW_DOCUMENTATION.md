# Fidalgo Hub - Documentação Técnica do Workflow v3

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Workflow](#arquitetura-do-workflow)
3. [Configuração de Secrets](#configuração-de-secrets)
4. [Estrutura de Dados](#estrutura-de-dados)
5. [Validações Implementadas](#validações-implementadas)
6. [Relatórios Gerados](#relatórios-gerados)
7. [Tratamento de Erros](#tratamento-de-erros)
8. [Performance](#performance)
9. [Extensões Futuras](#extensões-futuras)

---

## 🎯 Visão Geral

### Objetivo Principal
Automatizar validações semanais de dados de governança financeira e familiar, sincronizar com Notion Database e notificar stakeholders sobre o status das validações.

### Stack Técnico
- **Orquestração:** GitHub Actions
- **Linguagem:** Python 3.11
- **Integração:** Notion API
- **Notificação:** Gmail SMTP
- **Armazenamento:** GitHub Artifacts (30 dias)
- **Schedule:** Cron expression (domingo 22:00 UTC)

### Fluxo de Execução
```
┌─────────────────────────────────────────────────────────┐
│ GitHub Actions Schedule (domingo 22:00 UTC)             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ Checkout Repositório│
        └──────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │ Debug: Arquivos    │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │ Setup Python 3.11   │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │ Instalar Deps       │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │ Debug: Secrets      │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────────────┐
         │ Executar Script Python      │
         │ ├─ Validação dados         │
         │ ├─ Sync Notion             │
         │ ├─ Gerar relatórios        │
         │ └─ Enviar emails           │
         └──────────┬──────────────────┘
                    │
         ┌──────────▼──────────┐
         │ Upload Artefatos    │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │ Status: SUCCESS/    │
         │ WARNING/FAIL        │
         └─────────────────────┘
```

---

## ⚙️ Arquitetura do Workflow

### Job Principal: `weekly-validation`

```yaml
jobs:
  weekly-validation:
    name: Validação + Notion + Email Condicional
    runs-on: ubuntu-latest
    
    steps:
      1. Checkout do código
      2. Mostrar estrutura de arquivos (Debug)
      3. Configurar Python 3.11
      4. Instalar dependências
      5. Verificar Secrets (Debug)
      6. Executar Validação Automática
      7. Upload dos Relatórios Gerados
```

### Triggers

**Schedule (Automático)**
```yaml
on:
  schedule:
    - cron: '0 22 * * 0'  # Domingo 22:00 UTC
```

**Manual (Sob Demanda)**
```yaml
on:
  workflow_dispatch
```

---

## 🔐 Configuração de Secrets

### Secrets Obrigatórios (5 Total)

| Secret | Tipo | Fonte | Formato |
|--------|------|-------|---------|
| `NOTION_TOKEN` | API | Notion Settings | `secret_xxxxxxxx...` |
| `NOTION_DATABASE_ID` | ID | Notion URL | 32 caracteres hex |
| `GMAIL_USER` | Email | Gmail | `usuario@gmail.com` |
| `GMAIL_APP_PASSWORD` | Senha | Google Account | 16 chars + espaço |
| `RECIPIENT_EMAIL` | Email | Seu domínio | `destinatario@...` |

### Secrets Opcionais (1 Total)

| Secret | Tipo | Uso |
|--------|------|-----|
| `CC_EMAIL` | Email | Cópia no email de notificação |

### Injeção de Secrets no Workflow

```yaml
env:
  NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
  NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
  GMAIL_USER: ${{ secrets.GMAIL_USER }}
  GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
  RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
  CC_EMAIL: ${{ secrets.CC_EMAIL }}
```

---

## 📁 Estrutura de Dados

### Template JSON: `template_dados_completo.json`

**Tamanho:** ~500 bytes  
**Formato:** JSON FLAT (sem aninhamento)  
**Campos:** 20 principais

#### Categoria: Pessoa Física (PF)
```json
{
  "renda_mensal_pf": 8000,           // Renda mensal bruta
  "despesas_mensais_pf": 5000,       // Despesas mensais
  "prestacoes_mensais_total": 0,     // Prestações em dívida
  "caixa_aplicacoes_total": 55000,   // Total em caixa + aplicações
  "fluxo_real_mensal": 10500,        // Fluxo real observado
  "fluxo_projetado_mensal": 10000    // Fluxo esperado/orçado
}
```

#### Categoria: FSE (Fundo de Separação Familiar)
```json
{
  "distribuicoes_mensais_fse": 8000,      // Distribuições mensais
  "faturamento_bruto_mensal_fse": null,   // Faturamento (se aplicável)
  "custos_operacionais_fse": null,        // Custos operacionais
  "saldo_dividas_total": 0                // Saldo de dívidas
}
```

#### Categoria: Eletroposto
```json
{
  "eletroposto_capex_total": 1500000,        // Capital investido
  "eletroposto_receitas_anuais_proj": 400000,// Receitas projetadas
  "eletroposto_custos_anuais_proj": 150000   // Custos projetados
}
```

#### Categoria: Imóveis
```json
{
  "imoveis_count": 4,                          // Quantidade de imóveis
  "casa_quitada": true,                        // Casa residencial quitada?
  "valor_mercado_estimado_imoveis": 2500000   // Valor total estimado
}
```

#### Categoria: Planejamento Sucessório
```json
{
  "ativos_transferidos_pct": 20,      // Percentual transferido
  "itcmd_estimado_economia": 120000   // Economia fiscal estimada
}
```

#### Categoria: Risco
```json
{
  "risco_score_macro": 3.0  // Score 0-10 de risco macroeconômico
}
```

---

## ✅ Validações Implementadas

### 1. Validação de Estrutura
- ✔️ Campos obrigatórios presentes
- ✔️ Tipos de dados corretos
- ✔️ Valores dentro de ranges esperados

**Saída em caso de FAIL:**
```
❌ ESTRUTURA: Campo obrigatório faltando
```

### 2. Validação de Fluxo de Caixa
- ✔️ Fluxo real vs projetado (tolerância ±10%)
- ✔️ Cobertura de despesas (margem mínima 10%)
- ✔️ Tendência do caixa

**Saída em caso de WARNING:**
```
⚠️ FLUXO: Divergência de 15% entre real e projetado
```

### 3. Validação de Patrimônio
- ✔️ Quantidade e valores de imóveis
- ✔️ Estado de quitação
- ✔️ Valores compatíveis com mercado

**Saída em caso de FAIL:**
```
❌ PATRIMÔNIO: Valor incoerente com média de mercado
```

### 4. Validação de Eletroposto
- ✔️ CAPEX vs receitas
- ✔️ Cálculo de payback (máximo 10 anos)
- ✔️ Margem de lucro

**Saída em caso de WARNING:**
```
⚠️ ELETROPOSTO: Payback acima de 10 anos (12 anos estimado)
```

### 5. Validação de Planejamento Sucessório
- ✔️ Percentual transferido válido (0-100%)
- ✔️ Economia ITCMD coerente
- ✔️ Documentação mínima

**Saída em caso de SUCCESS:**
```
✅ SUCESSÓRIO: Planejamento dentro dos parâmetros
```

---

## 📄 Relatórios Gerados

### Formato 1: JSON (`validation_report_YYYYMMDD_HHMMSS.json`)

```json
{
  "timestamp": "2026-06-29T22:00:00Z",
  "status": "SUCCESS",
  "duracao_segundos": 45,
  
  "resumo_validacoes": {
    "total": 5,
    "sucesso": 4,
    "warning": 1,
    "fail": 0
  },
  
  "validacoes": [
    {
      "tipo": "ESTRUTURA",
      "status": "SUCCESS",
      "mensagem": "✅ Estrutura validada com sucesso",
      "detalhes": {
        "campos_validados": 20,
        "campos_obrigatorios_ok": true
      }
    },
    {
      "tipo": "FLUXO",
      "status": "SUCCESS",
      "mensagem": "✅ Fluxo de caixa dentro do esperado"
    },
    {
      "tipo": "PATRIMONIO",
      "status": "SUCCESS",
      "mensagem": "✅ Patrimônio imobiliário validado"
    },
    {
      "tipo": "ELETROPOSTO",
      "status": "WARNING",
      "mensagem": "⚠️ Eletroposto com receitas abaixo do esperado",
      "detalhes": {
        "receita_projetada": 400000,
        "receita_realizada": 350000,
        "divergencia_pct": 12.5
      }
    },
    {
      "tipo": "SUCESSORIO",
      "status": "SUCCESS",
      "mensagem": "✅ Planejamento sucessório validado"
    }
  ],
  
  "dados_resumo": {
    "patrimonio_total": 2500000,
    "fluxo_mensal": 10500,
    "eletroposto_payback_anos": 3.75,
    "economia_itcmd": 120000
  },
  
  "notion_sync": {
    "status": "OK",
    "registros_atualizados": 5,
    "timestamp_sync": "2026-06-29T22:05:30Z"
  },
  
  "email_notificacao": {
    "enviado": true,
    "tipo": "WARNING",
    "destinatario": "user@example.com",
    "cc": "cc@example.com"
  }
}
```

### Formato 2: Markdown (`validation_report_YYYYMMDD_HHMMSS.md`)

```markdown
# 📊 Relatório de Validação - Fidalgo Hub

**Data:** 29/06/2026 22:00 UTC  
**Status:** ⚠️ WARNING  
**Duração:** 45 segundos

---

## 📈 Resumo das Validações

| Validação | Status | Detalhes |
|-----------|--------|----------|
| ESTRUTURA | ✅ SUCCESS | 20 campos validados |
| FLUXO | ✅ SUCCESS | Dentro dos parâmetros |
| PATRIMÔNIO | ✅ SUCCESS | 4 imóveis, R$ 2.5M |
| ELETROPOSTO | ⚠️ WARNING | Receitas 12.5% abaixo |
| SUCESSÓRIO | ✅ SUCCESS | Planejamento OK |

---

## 🔍 Detalhes por Validação

### ✅ ESTRUTURA
Todos os 20 campos obrigatórios presentes e válidos.

### ✅ FLUXO DE CAIXA
- Fluxo Real: R$ 10.500
- Fluxo Projetado: R$ 10.000
- Divergência: 5% ✅ (tolerância: ±10%)

### ✅ PATRIMÔNIO IMOBILIÁRIO
- Imóveis: 4
- Casa Residencial: Quitada ✅
- Valor Estimado: R$ 2.500.000

### ⚠️ ELETROPOSTO
- CAPEX: R$ 1.500.000
- Receita Projetada: R$ 400.000/ano
- Receita Realizada: R$ 350.000/ano
- Divergência: 12.5% ⚠️
- Payback: 3,75 anos ✅ (máximo: 10 anos)

**Ação Recomendada:** Revisar receitas de eletroposto

### ✅ PLANEJAMENTO SUCESSÓRIO
- Ativos Transferidos: 20%
- Economia ITCMD: R$ 120.000
- Status: OK ✅

---

## 🔗 Sincronização Notion

- ✅ Conectado com sucesso
- ✅ 5 registros atualizados
- ✅ Último sync: 29/06/2026 22:05:30

---

## 📧 Notificação por Email

- ✅ Email enviado para: user@example.com
- ✅ Cópia: cc@example.com
- ✅ Tipo: WARNING

---

## 💾 Dados Resumidos

| Métrica | Valor |
|---------|-------|
| Patrimônio Total | R$ 2.500.000 |
| Fluxo Mensal | R$ 10.500 |
| Payback Eletroposto | 3,75 anos |
| Economia ITCMD | R$ 120.000 |
| Risco Macro | 3.0 |

---

**Próxima Validação:** Domingo 22:00 UTC (29/07/2026)
```

---

## 🐛 Tratamento de Erros

### Níveis de Severidade

**SUCCESS** ✅
- Todas as validações passaram
- Sem alertas
- Sem notificação por email

**WARNING** ⚠️
- Validações passaram mas com alertas
- Requer atenção
- Email enviado com detalhes

**FAIL** ❌
- Uma ou mais validações falharam
- Requer ação imediata
- Email urgente enviado

### Recuperação Automática

```yaml
if: always()  # Sempre executa
```

Garante que:
- ✅ Artefatos são salvos mesmo com erros
- ✅ Email é enviado em caso de falha
- ✅ Logs ficam disponíveis para debug

---

## ⚡ Performance

### Tempo de Execução

| Step | Tempo Estimado |
|------|----------------|
| Checkout | 10s |
| Debug: Arquivos | 5s |
| Python Setup | 30s |
| Instalar Deps | 20s |
| Debug: Secrets | 5s |
| Validação | 120s (depende do script) |
| Upload Artefatos | 10s |
| **TOTAL** | **~200s (3-4 min)** |

### Otimizações Implementadas

✅ **Cache de Pip**
```yaml
cache: 'pip'
```
Reutiliza dependências instaladas

✅ **Sempre Executa**
```yaml
if: always()
```
Evita reprocessamento

✅ **Secrets Localizados**
Armazena apenas no GitHub (não no código)

---

## 🚀 Extensões Futuras

### v4.0
- [ ] Integração com Slack
- [ ] Dashboard de histórico com gráficos
- [ ] Alertas via SMS
- [ ] Validações customizáveis por usuário
- [ ] Machine Learning para previsões

### v5.0
- [ ] Integração com Power BI
- [ ] API REST para dados de validação
- [ ] Webhooks para integrações custom
- [ ] Suporte a múltiplas databases Notion
- [ ] Auditoria completa de mudanças

---

## 📞 Suporte Técnico

Para problemas:

1. Verifique logs: `Actions` → execução → cada step
2. Valide secrets: `Settings` → `Secrets and variables`
3. Confirme arquivos: `git ls-files`
4. Teste manualmente: `Run workflow`

---

**Versão:** v3 Final  
**Data:** 2026-06-29  
**Autor:** Ricardo Fidalgo - Fidalgo Hub  
**Status:** ✅ Production Ready
