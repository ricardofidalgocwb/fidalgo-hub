# Guia de Configuração - Fidalgo Hub GitHub Actions v3

## 🎯 Objetivo
Configurar o workflow semanal de validação automática com notificações por email e sincronização com Notion.

---

## 📋 Checklist de Configuração

### ✅ Passo 1: Verificar Arquivos Necessários
- [ ] `validate_and_sync_notion_v2_final.py` existe no root
- [ ] `template_dados_completo.json` existe no root
- [ ] `.github/workflows/weekly_metrics_validation.yml` existe

### ✅ Passo 2: Configurar Secrets

**Acesse:** `Settings` → `Secrets and variables` → `Actions`

#### 2.1 NOTION_TOKEN
1. Acesse: https://www.notion.so/my-integrations
2. Crie uma nova integração
3. Copie o "Internal Integration Token"
4. Adicione como secret: `NOTION_TOKEN`

#### 2.2 NOTION_DATABASE_ID
1. Abra a database no Notion
2. Copie o ID da URL: `https://www.notion.so/{database-id}?v=...`
3. Adicione como secret: `NOTION_DATABASE_ID`

#### 2.3 GMAIL_USER
1. Use seu email Gmail
2. Exemplo: `seu-email@gmail.com`
3. Adicione como secret: `GMAIL_USER`

#### 2.4 GMAIL_APP_PASSWORD
⚠️ **IMPORTANTE:** Use senha de app, NÃO sua senha de conta

1. Ative 2FA na sua conta Google
2. Acesse: https://myaccount.google.com/apppasswords
3. Selecione: Mail + Windows Computer (ou seu device)
4. Copie a senha gerada (16 caracteres com espaço)
5. Adicione como secret: `GMAIL_APP_PASSWORD`

#### 2.5 RECIPIENT_EMAIL
1. Email que receberá as notificações
2. Exemplo: `seu-email@gmail.com` ou `outro-email@empresa.com`
3. Adicione como secret: `RECIPIENT_EMAIL`

#### 2.6 CC_EMAIL (Opcional)
1. Email adicional em cópia
2. Pode deixar em branco se não usar
3. Adicione como secret: `CC_EMAIL`

---

## 🧪 Teste do Workflow

### Teste 1: Execução Manual
1. Vá em `Actions`
2. Selecione `Fidalgo Hub - Validação Semanal de Métricas (v3 Final)`
3. Clique em `Run workflow`
4. Escolha a branch `main`
5. Clique em `Run workflow`

**Resultados esperados:**
- ✅ Debug: Lista arquivos do repositório
- ✅ Debug: Mostra status dos secrets (✅ ou ❌)
- ✅ Python 3.11 configurado
- ✅ Dependências instaladas
- ✅ Script Python executado
- ✅ Relatórios gerados
- ✅ Email enviado (se WARNING ou FAIL)

### Teste 2: Verificar Logs
1. Clique no workflow que rodou
2. Expanda cada step para ver detalhes
3. Procure por erros ou warnings

### Teste 3: Verificar Artefatos
1. No workflow run, vá em `Artifacts`
2. Baixe `weekly-validation-reports`
3. Verifique se contém:
   - `validation_report_*.json`
   - `validation_report_*.md`

### Teste 4: Email
1. Verifique sua caixa de entrada
2. Procure por: `⚠️ Fidalgo Hub - Validação Semanal` ou `❌ Fidalgo Hub`
3. Clique no link do workflow para validar

---

## 🔍 Troubleshooting

### ❌ Erro: "validate_and_sync_notion_v2_final.py NÃO ENCONTRADO"

**Solução:**
```bash
# Verifique se o arquivo existe no root
git ls-files | grep validate_and_sync_notion_v2_final.py

# Se não existir, adicione-o
git add validate_and_sync_notion_v2_final.py
git commit -m "feat: Adicionar script de validação"
git push
```

---

### ❌ Erro: "template_dados_completo.json NÃO ENCONTRADO"

**Solução:**
```bash
# Verifique se o arquivo existe no root
git ls-files | grep template_dados_completo.json

# Se não existir, o arquivo foi criado automaticamente
# Atualize o repositório localmente
git pull
```

---

### ❌ Erro: "NOTION_TOKEN definido: ❌ NÃO"

**Solução:**
1. Acesse: `Settings` → `Secrets and variables` → `Actions`
2. Clique em `New repository secret`
3. Nome: `NOTION_TOKEN`
4. Valor: Cole seu token do Notion
5. Clique em `Add secret`

**Repita para todos os 5 secrets obrigatórios.**

---

### ❌ Erro: "SMTP Authentication failed" (Email não enviado)

**Possíveis causas:**
1. `GMAIL_APP_PASSWORD` está errada
2. Você usou a senha de conta ao invés de app password
3. 2FA não está ativado

**Solução:**
1. Acesse: https://myaccount.google.com/apppasswords
2. Gere uma nova app password
3. Copie exatamente como gerado (16 chars + espaço)
4. Atualize o secret `GMAIL_APP_PASSWORD`

---

### ❌ Erro: "Script executa mas sem relatórios"

**Possíveis causas:**
1. Script não gera arquivos `validation_report_*`
2. Arquivos gerados em pasta diferente

**Solução:**
1. Verifique o script Python
2. Confirme que gera: `validation_report_*.json` e `validation_report_*.md`
3. Confirme que salva no root do repositório
4. Ajuste o workflow se necessário

---

## 📅 Agendamento

### Próximas Execuções Automáticas
- **Próximo domingo às 22:00 UTC (19:00 BRT)**
- Se hoje é domingo e já passou das 22:00 UTC, a próxima será em 7 dias

### Como Alterar o Schedule
Se quiser mudar o dia/hora:

1. Edite: `.github/workflows/weekly_metrics_validation.yml`
2. Altere a linha:
   ```yaml
   - cron: '0 22 * * 0'
   ```
3. Use o formato cron:
   ```
   ┌───────────── minuto (0 - 59)
   │ ┌───────────── hora (0 - 23)
   │ │ ┌───────────── dia do mês (1 - 31)
   │ │ │ ┌───────────── mês (1 - 12)
   │ │ │ │ ┌───────────── dia da semana (0 - 6) (domingo = 0)
   │ │ │ │ │
   │ │ │ │ │
   * * * * *
   ```

**Exemplos:**
- Segunda-feira às 9h: `0 9 * * 1`
- Quinta-feira às 15h: `0 15 * * 4`
- Diariamente às 12h: `0 12 * * *`
- A cada 6 horas: `0 */6 * * *`

---

## 📊 Monitoramento Contínuo

### 1. Ver Histórico de Execuções
- Acesse: `Actions` → `Fidalgo Hub - Validação Semanal`
- Visualize todas as execuções (automáticas e manuais)

### 2. Analisar Tendências
- Salve os relatórios semanais
- Compare: `validation_report_*.json`
- Identifique padrões de WARNING ou FAIL

### 3. Notificações por Email
- Status SUCCESS: Sem email (esperado)
- Status WARNING: Receba email de alerta
- Status FAIL: Receba email urgente

---

## 📚 Recursos Adicionais

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Notion API Documentation](https://developers.notion.com)
- [Gmail App Password Setup](https://support.google.com/accounts/answer/185833)
- [Cron Expression Generator](https://crontab.guru/)

---

## ✅ Verificação Final

Antes de considerar tudo pronto, verifique:

- [ ] Todos os 5 secrets configurados
- [ ] Arquivos necessários no root
- [ ] Workflow executado manualmente com sucesso
- [ ] Email recebido com notificação
- [ ] Artefatos gerados e disponíveis
- [ ] Próxima execução automática agendada para domingo

**Se tudo está ✅, a configuração está completa!** 🚀

---

**Versão:** v3 Final  
**Data:** 2026-06-29  
**Status:** ✅ Pronto para Produção
