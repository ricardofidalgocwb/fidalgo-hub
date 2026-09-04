# Fidalgo Hub - Estrutura do Projeto

## 📁 Organização

```
fidalgo-hub/
│
├── 📄 README.md
├── 📄 SETUP_GUIDE.md
├── 📄 WORKFLOW_DOCUMENTATION.md
├── 📄 FAQ.md
├── 📄 CHANGELOG.md
├── 📄 CONTRIBUTING.md
├── 📄 PROJECT_STRUCTURE.md
│
├── 🔧 Configuração
│   ├── .env.example
│   ├── .gitignore
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── setup.sh
│   └── test_local.sh
│
├── 🗂 config/
│   └── notion_ids.json                     # IDs canônicos Notion (sem secrets)
│
├── 🖥 dashboard/                             # Painel Founder + runner editorial · Heros Custom
│   ├── app.py                              # Flask local (dry-run padrão)
│   ├── status_machine.py                   # Aprovar / Avançar / Recusar / Adiar
│   ├── notion_fila.py                      # PATCH só na Fila Founder
│   ├── editorial_status.py                 # Aprovar ≠ publicar (Fila Editorial)
│   ├── editorial_canon.py                  # Canon travado; figura inventada bloqueia Aprovar
│   ├── editorial_runner.py                 # CLI dry-run; CONFIRM=1 só Status=Aprovado
│   ├── pulse.py
│   ├── templates/index.html
│   └── fixtures/
│       ├── sample_fila.json
│       └── sample_fila_editorial.json      # EDI-1 Datar / EDI-2 Anchieta
│
├── 🧪 tests/
│   ├── test_status_machine.py
│   ├── test_n8n_guard.py
│   ├── test_panel_http.py
│   ├── test_editorial_runner.py
│   └── test_editorial_canon.py
│
├── 🚀 Workflow
│   ├── .github/workflows/weekly_metrics_validation.yml
│   └── .github/workflows/founder_panel_tests.yml
│
├── 💻 Scripts
│   ├── validate_and_sync_notion_v2_final.py
│   └── scripts/drive_resumable_upload.py   # Path B Drive resumable; SSOT docs/drive-binary-upload.md
│
├── 📊 Dados
│   └── template_dados_completo.json
│
└── 🤖 agents/  leads/  sales/
```

O painel Founder estende este repositório (Python + Notion). Não é um segundo SSOT: só lê a Central de Comando e escreve Status / Data do OK / Observações na Fila Founder.

## 🎯 Arquivos Principais

### 📖 Documentação

| Arquivo | Propósito | Audience |
|---------|-----------|----------|
| `README.md` | Visão geral e quick start | Iniciantes |
| `SETUP_GUIDE.md` | Passo a passo de configuração | Novos usuários |
| `WORKFLOW_DOCUMENTATION.md` | Detalhes técnicos | Desenvolvedores |
| `FAQ.md` | Perguntas frequentes | Todos |
| `CHANGELOG.md` | Histórico de versões | Todos |
| `CONTRIBUTING.md` | Guia de contribuição | Contribuidores |
| `PROJECT_STRUCTURE.md` | Estrutura do projeto | Desenvolvedores |

### ⚙️ Configuração

| Arquivo | Propósito |
|---------|----------|
| `.env.example` | Exemplo de variáveis de ambiente |
| `.gitignore` | Arquivos a ignorar no git |
| `requirements.txt` | Dependências Python |
| `setup.sh` | Script de setup automático |
| `test_local.sh` | Script de testes locais |

### 🚀 Automação

| Arquivo | Propósito |
|---------|----------|
| `.github/workflows/weekly_metrics_validation.yml` | Workflow principal (v3.1.0) |

### 💻 Scripts Python

| Arquivo | Propósito | Versão |
|---------|-----------|--------|
| `validate_and_sync_notion_v2_final.py` | Script de validação completo | 2.0 Final |

### 📊 Dados

| Arquivo | Propósito |
|---------|----------|
| `template_dados_completo.json` | Template JSON para validação |

## 🔄 Fluxo de Trabalho

### Local (Desenvolvimento)

```
1. git clone https://github.com/ricardofidalgocwb/fidalgo-hub.git
2. bash setup.sh
3. Editar .env
4. Fazer mudanças no código
5. bash test_local.sh (testar)
6. git add . && git commit
7. git push origin feature/xyz
8. Abrir Pull Request
```

### GitHub (Automático)

```
1. Push para main
   ↓
2. Workflow dispara automaticamente
   ↓
3. Executa validações
   ↓
4. Gera relatórios
   ↓
5. Envia email (se WARNING/FAIL)
   ↓
6. Upload de artefatos
```

## 📋 Checklist para Novos Desenvolvedores

```
☐ Clonar repositório
☐ Ler README.md
☐ Ler SETUP_GUIDE.md
☐ Executar setup.sh
☐ Consultar FAQ.md para dúvidas
☐ Revisar WORKFLOW_DOCUMENTATION.md
☐ Fazer primeiro teste local
☐ Ler CONTRIBUTING.md antes de contribuir
```

## 🎯 Versões do Projeto

### Versão Atual: 3.1.0

```
v3.1.0 (2026-07-05)
├─ Workflow aprimorado com tratamento de erros
├─ Script Python com 5 validações
├─ Documentação completa
├─ FAQ com 40+ perguntas
├─ Scripts locais de setup e teste
└─ Guias de contribuição e estrutura

v3.0.0 (2026-06-29)
├─ Workflow v3 inicial
├─ Notificações por email
├─ Sincronização Notion
└─ Relatórios JSON/Markdown

v2.0.0 (Anterior)
└─ Versão descontinuada
```

## 🔐 Segurança

### Dados Sensíveis

```
❌ NUNCA commit:
- .env (use .env.example)
- Tokens API
- Senhas
- Chaves privadas

✅ SEMPRE use:
- GitHub Secrets
- Environment variables
- .env.example como referência
```

### Checklist de Segurança

```
☐ Não commitar .env
☐ Não adicionar tokens em commits
☐ Usar GitHub Secrets para workflow
☐ Validar entrada de dados
☐ Usar variáveis de ambiente
☐ Revisar logs para dados sensíveis
```

## 📈 Escalabilidade

### Estrutura para Crescimento

```
Futuro (v4.0+):
├─ /scripts/ (múltiplos scripts)
├─ /tests/ (testes unitários)
├─ /docs/ (documentação expandida)
├─ /src/ (código source organizado)
│   ├─ validators/
│   ├─ sync/
│   └─ reports/
└─ /config/ (arquivos de configuração)
```

## 🤝 Colaboração

### Como Contribuir

1. **Issues**: Reporte bugs ou sugira features
2. **Discussions**: Dúvidas e brainstorm
3. **Pull Requests**: Contribua com código

Ver `CONTRIBUTING.md` para detalhes.

## 📞 Contato

- **GitHub**: https://github.com/ricardofidalgocwb/fidalgo-hub
- **Issues**: https://github.com/ricardofidalgocwb/fidalgo-hub/issues
- **Discussions**: https://github.com/ricardofidalgocwb/fidalgo-hub/discussions

## 📚 Recursos

- [GitHub Docs](https://docs.github.com)
- [Python Best Practices](https://peps.python.org/pep-0008/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Semantic Versioning](https://semver.org/)

---

**Última atualização:** 2026-07-05  
**Versão:** 3.1.0  
**Status:** ✅ Production Ready
