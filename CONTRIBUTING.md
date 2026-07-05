# Contribuindo para o Fidalgo Hub

Agradecemos seu interesse em contribuir! Este documento descreve como fazer isso.

## 🐛 Reportar Bugs

### Antes de Reportar
- [ ] Verifique se o bug já foi reportado (Issues)
- [ ] Teste com a versão mais recente
- [ ] Consulte a documentação (FAQ, SETUP_GUIDE)

### Como Reportar
Abra uma Issue com:
1. **Título claro** - Descreva o problema em poucas palavras
2. **Descrição** - Explique em detalhes
3. **Passos para reproduzir** - Liste os passos
4. **Comportamento esperado** - O que deveria acontecer
5. **Comportamento atual** - O que está acontecendo
6. **Ambiente** - Python, OS, versão do repo
7. **Logs** - Inclua logs relevantes

### Exemplo
```
Título: Script falhando com NOTION_TOKEN inválido

Descrição:
O script não valida o NOTION_TOKEN antes de usar

Passos para reproduzir:
1. Configurar NOTION_TOKEN com valor inválido
2. Executar: python validate_and_sync_notion_v2_final.py
3. Observar erro genérico

Esperado:
Mensagem clara: "NOTION_TOKEN inválido ou expirado"

Atual:
ConnectionError genérico sem contexto
```

## 💡 Sugerir Melhorias

### Antes de Sugerir
- [ ] Verifique se a sugestão já existe (Discussions)
- [ ] Considere se faz sentido com os objetivos do projeto

### Como Sugerir
Abra uma Discussion com:
1. **Descrição clara** da melhoria
2. **Motivação** - Por que isso seria útil?
3. **Exemplo de uso** - Como seria usado
4. **Alternativas consideradas** - Outras abordagens
5. **Impacto** - Que mudanças exigira

## 🔧 Contribuir com Código

### Requisitos
- [ ] Python 3.11+
- [ ] Git configurado
- [ ] Conhecimento de GitHub Workflows (opcional)

### Processo

#### 1. Fork e Clone
```bash
git clone https://github.com/SEU_USERNAME/fidalgo-hub.git
cd fidalgo-hub
git remote add upstream https://github.com/ricardofidalgocwb/fidalgo-hub.git
```

#### 2. Criar Branch
```bash
git checkout -b feature/sua-feature
# ou
git checkout -b fix/seu-bug
```

#### 3. Fazer Mudanças
- Siga o estilo de código existente
- Mantenha commits pequenos e claros
- Escreva boas mensagens de commit

#### 4. Testar
```bash
# Setup local
bash setup.sh

# Executar testes
bash test_local.sh

# Validar antes de push
python validate_and_sync_notion_v2_final.py --input template_dados_completo.json
```

#### 5. Commit e Push
```bash
git add .
git commit -m "feat: Descrição da mudança"
git push origin feature/sua-feature
```

#### 6. Pull Request
- Abra PR contra `main`
- Preencha o template do PR
- Referencie issues relacionadas (#123)
- Aguarde revisão

## 📋 Guia de Estilo

### Python
```python
# ✅ BOM
def validar_estrutura(dados):
    """Valida estrutura dos dados."""
    campos_faltando = []
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in dados:
            campos_faltando.append(campo)
    return len(campos_faltando) == 0

# ❌ RUIM
def validate(d):
    m = []
    for f in FIELDS:
        if f not in d: m.append(f)
    return len(m)==0
```

### Commits
```
✅ BOM
feat: Adicionar validação de fluxo de caixa
fix: Corrigir parsing de NOTION_DATABASE_ID
docs: Atualizar FAQ com novo exemplo
refactor: Simplificar lógica de validação
chore: Atualizar requirements.txt

❌ RUIM
update
fix stuff
novo código
trabalho em progresso
```

### Documentação
- Use Markdown
- Inclua exemplos
- Mantenha atualizado
- Estruture com headings

## 🎯 Roadmap de Desenvolvimento

### v3.1.1 (Bugfixes)
- [ ] Melhorar tratamento de exceções
- [ ] Validar edge cases
- [ ] Otimizar performance

### v3.2.0 (Features)
- [ ] Suporte a múltiplas databases
- [ ] Validações customizáveis
- [ ] Análise de tendências

### v4.0 (Major)
- [ ] Integração Slack
- [ ] Dashboard interativo
- [ ] API REST

## 📚 Recursos Úteis

- [GitHub Docs](https://docs.github.com)
- [Python Docs](https://docs.python.org/3/)
- [Notion API](https://developers.notion.com)
- [Keep a Changelog](https://keepachangelog.com)

## 🤝 Código de Conduta

Todos são bem-vindos! Mantenha respeito e profissionalismo.

## 📞 Dúvidas?

- Abra uma Issue
- Abra uma Discussion
- Consulte a documentação

---

**Obrigado por contribuir! 🙏**
