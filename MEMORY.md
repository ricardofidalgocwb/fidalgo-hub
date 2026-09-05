# Fidalgo Hub - Memorial Descritivo Completo

## Dashboard Founder (decisão 26/08/2026)
- Painel interno no repo: `dashboard/` · marca **Heros Custom**
- Notion SSOT = Fila Founder (`01cb462a…`)
- Aprovar = Aguardando OK → Aprovado, sem n8n
- Avançar = Aprovado → Em Execução; n8n opcional e desligado por padrão
- Não escrever OS Status Entregue; não usar Leads arquivado 43b3f514
- Não misturar CNPJ/caixa Heros vs FSE

## Runner editorial Editora × Produtora (decisão 26/08/2026)
- SSOT = Fila Editorial (`8af724e1…` / ds `13be9ea3…`), parent Mesa editorial (`3c97d36b…`)
- Módulo separado: `dashboard/editorial_runner.py` — não é bot novo, não é quarta marca
- Dry-run padrão; `CONFIRM=1` só grava Status=Aprovado (e talvez Observações)
- **Aprovar ≠ publicar.** Publicado só o Ricardo. Canal Não publicar permanece
- Sem n8n, IG, PDF, site. Sem escrita em Fila Founder / OS / CRM / Clientes / Financeiro
- Peças vivas: EDI-1 Kit Datar (M0 D1), EDI-2 Reel Anchieta 1959
- Sincronismo: 12 V BR = 1968; 12 V não implica alternador; fim BR = 1996 (2003 = México)
- Anchieta nacional 03/01/1959; planta 18/11/1959; Ipiranga CKD 2.268; Itamar 47.700
- Canon em `dashboard/editorial_canon.py`: figura fora da lista bloqueia Aprovar; sem pacote `editorial/`

## Drive binário ≥100 KB (04/09/2026)
- SSOT: `docs/drive-binary-upload.md` — Operações / Entrega / Comunicação
- Allowlist MCP: `docs/mcp-drive-allowlist.md` — `search` / `get_file_metadata` ok; **proibido** `create_file` para imagem/vídeo de evidência
- Aceite só `size` > 100 000 bytes (metadado Drive). Stub = recusar. Audit offline: `scripts/drive_evidence_audit.py`
- Path A (preferido): Ricardo drop manual no browser em OS-34 `00_Antes` (`1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-`)
- Path B: `scripts/drive_resumable_upload.py` (resumable, não MCP). Auth local só — ver `scripts/README.md`. Sem secrets no git
- Sem n8n Active, sem placeholder, sem publish, sem escrita Notion neste fluxo
- Audit 2026-09-04 (America/Sao_Paulo): `00_Antes` tem **17 solid** (>100000 bytes) e **0 stubs**. Caixa presente: `AIW3138_00_Antes_10_caixa_fusiveis_print_zap.png` (~2.8 MB, id `1qO4OS7GdJAfmxUrvH0PbosEgGKjvtICC`). Inbox `00_Cliente_envia` vazia de ficheiros. IDs em `config/drive_ids.json`
- Twin Notion: HC-2026-025 (Nº35 ICE) e OS-34 (Nº34 comercial) partilham a pasta Drive. Passaporte dual: cabeça ds `a0254a75…` / linhas ds `d2d7d36b…` — write=false
- COM-PDF-02 embed fotográfico continua **HOLD** até follow-up explícito (não inventar `<img>`)

## COM-PDF-APR-N0 Aprendiz (04/09/2026)
- Pasta unpublished `docs/propostas/COM-PDF-APR-N0/` — HTML+print CSS+PDF, Camada A (Type 1 / N0) + Camada B esqueleto
- Sem site até OK Founder. Aprendiz testa como aluno. Slots foto-modelo AUSENTE. Sem carro tipado
- Canon: 12 V BR=1968; 12 V ≠ alternador; fim BR=1996; 1º nacional 03/01/1959; Anchieta 18/11/1959
- Sem OS viva / CPF / preço / diagrama Type 3 de ensino / os 9 procedimentos. Hércules = método, não nome do curso
- CTA: M1 chicote · ou OS box (hold COM) — sem telefone/NAP no PDF até OK COM. Gold v1.1
- COS P0: Quiz D1 sem marca no corpo; gabarito só no fim; ☐ no checklist; linhas A1–A6

## COM-PDF-02 Theodoro (04/09/2026)
- Pasta unpublished `docs/propostas/COM-PDF-02-theodoro/` — HTML+print CSS, sem foto embutida
- Pacote A R$ 1.850 / B R$ 4.200; F0–F8 = previsão de bancada; cobrança = pacote
- Fotos Drive (2026-09-04): `00_Antes` **não** está vazio — 17 solid + caixa ~2.8 MB. Slots no HTML continuam AUSENTE. Embed no PDF = HOLD até PR de follow-up explícito
- Upload de novas provas: `docs/drive-binary-upload.md` + allowlist MCP (não `create_file`)
- Não enviar ao cliente, não implantar, sem CPF / URL Notion / IG / n8n no artefato
- COM-ALIGN-01: Gold v1.1 — `#C9A227` / carbon `#0D0D0D` / panel `#1A1A1A` / paper `#F5F0E6`

## Objetivo Geral
Central inteligente multicanal que gerencia múltiplos agentes de IA para atendimento, operações e geração de leads das empresas do grupo Fidalgo.

## Conselho Total
- RFidalgo — Fundador e decisor final

## Regras de Realimentação e Revisão
- Todo agente deve ler este arquivo MEMORY.md antes de iniciar qualquer tarefa
- Realizar revisão, recálculo e realimentação a cada nova demanda
- Atualizar constantemente os próximos requisitos e prioridades
- Registrar toda decisão neste arquivo

## Canais Integrados
- WhatsApp (canal principal)
- Instagram
- TikTok
- Outras redes sociais

## Função dos Agentes
Os agentes estarão preparados para:
- Receber informações em tempo real
- Analisar dados de conversas e interações
- Projetar estratégias de marketing e branding
- Identificar e qualificar próximos leads da operação
- Gerar conteúdo e campanhas alinhadas com o branding

## Funcionalidades Principais
- Gerenciamento e calibração de dashboard em tempo real
- Coleta automática e estruturada de dados
- Diagnóstico técnico inteligente
- Lógica de decisão integrada

## Arquitetura do Sistema
- Central de Orquestração multicanal
- Múltiplos agentes especializados
- Dashboard em tempo real para monitoramento
- Memória compartilhada via GitHub

## Operações
- Atendimento 24/7 em múltiplos canais
- Geração e qualificação inteligente de leads
- Criação de conteúdo e estratégias de marketing
- Atualização contínua do status de todas as demandas

**Status do Projeto:** Iniciado - Maio 2026
**Regra de Ouro:** Sempre revisar, recalcular e realimentar este arquivo antes de qualquer nova ação.