## Changelog - Fidalgo Hub

Todos as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased] - VIS tipadas H1 / VIS-G1 + M6_T (unpublished)

### Adicionado
- `docs/acervo/vis-tipadas/`: três JPEGs Commons SRC ≥100 KB (H1×2 gênese + M6 tronco T único)
- `SOURCES.md` + `README.md` com mapa VIS-G1/H1×2 + M6_T, Drive IDs e índice VIS
- Guarda `tests/test_vis_tipadas_h1_m6.py` (existência + ≥100000; DUPs/HenryFord fora; N0-H1 Era B1 intacta)
- Pacote separado de Cap.2 / N0 A.8. Não publicar

---

## [Unreleased] - COM-PDF-CAP2-motor Cap. 2 boxer a ar (unpublished)

### Adicionado
- `docs/propostas/COM-PDF-CAP2-motor/`: pacote HTML+print CSS+PDF do Cap. 2 — Anatomia do motor boxer a ar (Type 1, rascunho 0.2)
- Miolo Acervo §§1–5, checklist Aprendiz 1–8 ☐, quiz «nomeie a peça» 10Q (gabarito só no fim), ponte N0 (item 9)
- Guarda em `tests/test_com_pdf_cap2.py` (Gold v1.1, sem Theodoro/Herculid/ISBN/NAP/WhatsApp/preço, sem ✅ nas opções)
- Pacote separado do COM-PDF-APR-N0. Não publicar / sem site até OK Founder

---

## [Unreleased] - COM-PDF-APR-N0 Aprendiz (unpublished)

### Adicionado
- `docs/propostas/COM-PDF-APR-N0/`: pacote HTML+print CSS+PDF do curso inicial elétrica simples (N0) Type 1
- Camada A completa (6 aulas, A1–A6, §10, Quiz D1 placeholder, checklist 1–7, E1–E3, slots AUSENTE)
- Camada B esqueleto: só com Passaporte tipado; campos vazios; sem carro
- Guarda em `tests/test_com_pdf_apr_n0.py` (Gold v1.1, sem Theodoro/Diogo/CPF/Herculid, sem diagrama Type 3 de ensino)
- Não publicar / sem site até OK Founder. Aprendiz testa como aluno
- QA Aprendiz: Quiz D1 10Q + gabarito editorial embutidos; A1–A6 = texto N0 §9 exato
- COS P0: Quiz sem ✅ no corpo (gabarito só no fim); checklist ☐; linhas A1–A6; CTA hold COM (sem telefone)
- CTA miolo: Próximo: M1 chicote — ou agendar diagnóstico (sem NAP/WhatsApp); slots A.8 hold Founder/Ops; ○ vazia A/B/C

---

## [Unreleased] - Audit Drive OS-34 + IDs (unpublished)

### Adicionado
- `config/drive_ids.json`: árvore OS-34 (`root` / `02_Fotos` / `00_Antes` / `00_Cliente_envia`) + catálogo de tipagem + caixa ~2.8 MB. Twin partilha pasta. Sem secrets
- `scripts/drive_evidence_audit.py` + `tests/test_drive_evidence_audit.py`: portão stub (≤100000) vs solid, manifesto `--manifest`, gaps de tipagem; exit ≠ 0 se houver stub. Dry-only, sem Drive live
- `docs/mcp-drive-allowlist.md`: bots podem `search` / `get_file_metadata`; `create_file` de imagem/vídeo proibido; Path A manual / Path B resumable

### Alterado
- `config/notion_ids.json`: fetched_at 2026-09-04; páginas COMECE AQUI; DBs Passaporte cabeça/linhas; twin HC-2026-025=ICE / OS-34=comercial / Drive partilhado; write=false em OS/CRM/Clientes/Passaporte; Fila Editorial write=false runner_only
- `MEMORY.md` e `docs/propostas/COM-PDF-02-theodoro/README.md`: `00_Antes` tem 17 solid + caixa ~2.8 MB (2026-09-04); embed PDF continua HOLD; MCP `create_file` continua banido. HTML da proposta sem `<img>`

---

## [Unreleased] - Upload Drive binário ≥100 KB (unpublished)

### Adicionado
- `docs/drive-binary-upload.md`: SSOT para Operações / Entrega / Comunicação — **proibido** MCP Drive `create_file` / base64 em foto ou vídeo de evidência (G-FOTO / Passaporte / Antes)
- Aceite só ficheiro com `size` > 100 000 bytes (metadado Drive). Path A = drop manual do Ricardo em OS-34 `00_Antes`; Path B = script resumable
- `scripts/drive_resumable_upload.py`: upload Drive **resumable** (não MCP); recusa local ≤100 KB; `--dry-run` sem API; lixeira se o remoto for stub
- `tests/test_drive_resumable_upload.py`: portão de tamanho sem Drive live
- Sem n8n Active, sem publish, sem secrets no git. COM-PDF-02 continua à espera do drop real

---

## [Unreleased] - COM-PDF-02 Theodoro (unpublished, texto)

### Adicionado
- `docs/propostas/COM-PDF-02-theodoro/`: proposta HTML+print CSS da Heros Custom para Variant AIW3138
- Primeira passagem **só texto**; slots fotográficos AUSENTE; não enviar ao cliente; não implantar
- Pacotes travados A R$ 1.850 / B R$ 4.200; tabela F0–F8 como previsão de bancada
- Guarda em `tests/test_com_pdf_02.py` (sem CPF, Notion URL, IG, n8n, Type 1, `<img>`)
- COM-ALIGN-01: `print.css` travado em Gold v1.1 (`#C9A227` / `#0D0D0D` / `#1A1A1A` / `#F5F0E6`)

---

## [3.3.1] - 2026-09-03 - Canon guard no runner editorial

### Adicionado
- `dashboard/editorial_canon.py`: recusa mito (12 V=1967, 12 V≠alternador, fim BR=2003, Anchieta com data trocada) e figura inventada (ex.: “2 milhões”)
- Aprovar (e o dry-run planejado) bloqueia card fora do canon; volumes cravados: Ipiranga CKD 2.268, Itamar 47.700
- `docs/editorial-runner.md` descreve o runner de `main` (`python -m dashboard.editorial_runner`): Aprovar nunca publica, Publicado só do Ricardo, sem n8n/IG/PDF/site

---

## [3.3.0] - 2026-08-27 - Runner editorial (Editora × Produtora)

### Adicionado
- Runner dry-run `python -m dashboard.editorial_runner` para a Fila Editorial (Heros Editora × Produtora)
- Máquina de status: Rascunho / Aguardando OK → Aprovado; Recusar → Recusado
- **Aprovar ≠ publicar:** o runner recusa Status=Publicado, não altera Canal, não dispara n8n
- `fila_editorial` em `config/notion_ids.json` com `write=false` / `runner_only=true`
- Fixtures EDI-1 (kit Datar) e EDI-2 (reel Anchieta) para CI sem Notion live

---

## [3.2.0] - 2026-08-26 - Painel Founder (Heros Custom)

### Adicionado
- Painel Founder local (`python -m dashboard.app`) com pulso Notion e botões Aprovar / Avançar / Recusar / Adiar
- Máquina de status alinhada ao schema vivo da Fila Founder
- Dry-run padrão; escrita só com `NOTION_TOKEN` + `CONFIRM=1` ou confirmação na UI
- Aprovar nunca dispara n8n; Avançar só dispara webhook se `N8N_AVANCAR_ENABLED=1`
- `config/notion_ids.json` com IDs canônicos (CRM 6157d36b…, OS e1a7d36b…, sem Leads 43b3f514)
- Testes em `tests/` e workflow `founder_panel_tests.yml`

---

## [3.1.0] - 2026-06-29 - Aprimoramentos de Tratamento de Erros

### ✨ Adicionado
- ✅ Exit code handling no step de validação
- ✅ Captura completa de logs de execução
- ✅ Validação prévia de arquivos necessários
- ✅ Timestamps em toda execução
- ✅ Timeout global (15 minutos) para o job
- ✅ Verificação de dependências instaladas
- ✅ Sumário expandido com links úteis
- ✅ Melhor contexto nos emails de notificação

### 🐛 Corrigido
- ✅ Script Python falhando silenciosamente
- ✅ Falta de logs de erro capturados
- ✅ Emails sem contexto suficiente
- ✅ Erro de digitação em README.md ("guardama" → "guardam")
- ✅ Falta de validação de arquivos antes da execução

### 🔧 Melhorado
- ✅ Melhor tratamento de exceções
- ✅ Logs mais detalhados e estruturados
- ✅ Emails com informações mais completas
- ✅ Sumário do workflow com mais contexto
- ✅ Step de instalação de deps com verificação

### 📋 Técnico
- Adicionado `timeout-minutes: 15` ao job
- Adicionado `if-no-files-found: warn` ao upload de artefatos
- Adicionado validação de arquivos em novo step
- Melhorado script de extração de status com tratamento de arquivo faltante
- Expandido sumário do GitHub com links e detalhes

---

## [3.0.0] - 2026-06-29 - Versão Final (v3 Production Ready)

### ✨ Adicionado
- ✅ Workflow GitHub Actions v3 completo
- ✅ Validação automática semanal (domingo 22:00 UTC)
- ✅ Notificações condicionais por email (WARNING/FAIL)
- ✅ Sincronização com Notion Database
- ✅ Geração de relatórios JSON + Markdown
- ✅ Debug steps para troubleshooting
- ✅ Verificação de secrets
- ✅ Upload de artefatos (30 dias)
- ✅ Template JSON com dados de teste
- ✅ Documentação completa (3 documentos)

### 📚 Documentação
- ✅ README.md - Visão geral e quick start
- ✅ SETUP_GUIDE.md - Passo a passo de configuração
- ✅ WORKFLOW_DOCUMENTATION.md - Documentação técnica
- ✅ CHANGELOG.md - Este arquivo

### 🔐 Segurança
- ✅ Secrets encriptados do GitHub
- ✅ Nenhuma credencial no código
- ✅ Masking automático de secrets em logs
- ✅ Validação de integridade de dados

### ⚡ Performance
- ✅ Cache de pip para otimização
- ✅ Python 3.11 para performance
- ✅ Execução em ~3-4 minutos

---

## [2.0.0] - Data anterior (Versão anterior)

- Versão anterior do sistema

---

## Contribuindo

Para relatar bugs ou sugerir melhorias:

1. Abra uma [Issue](https://github.com/ricardofidalgocwb/fidalgo-hub/issues)
2. Descreva claramente o problema
3. Forneça exemplos se possível

---

## Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/):

- **MAJOR**: Mudanças incompatíveis (ex: v2.0.0 → v3.0.0)
- **MINOR**: Novas funcionalidades compatíveis (ex: v3.0.0 → v3.1.0)
- **PATCH**: Correções de bugs (ex: v3.1.0 → v3.1.1)

---

**Última atualização:** 2026-06-29  
**Versão atual:** 3.1.0  
**Status:** ✅ Production Ready
