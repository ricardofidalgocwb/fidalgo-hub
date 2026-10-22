# gf-core

App **local e unpublished** de gestão multi-entidade da Holding Grupo Fidalgo, com foco na operação industrial da **Eletro Fidalgo (EF)**. Roda na máquina de quem opera. Não publica site, não aponta domínio, não chama planilha remota, não integra n8n e não usa Hotmart.

Não há carga inicial. O banco nasce vazio. Não coloque CNPJ, preço ou cliente real neste repositório.

## Como rodar

Na pasta `apps/gf-core`, com Python 3.11:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# API local — documentação em http://127.0.0.1:8077/docs
uvicorn api.app:app --host 127.0.0.1 --port 8077

# Painel (outro terminal, mesmo venv)
streamlit run ui/streamlit_app.py --server.address 127.0.0.1 --server.port 8078
```

O sqlite fica em `apps/gf-core/data/grupo_fidalgo.db` (gitignored). Outro arquivo: `GF_CORE_DB=/caminho/grupo_fidalgo.db`.

Os testes de domínio entram no job já existente do painel Founder, sem instalar FastAPI:

```bash
python -m pytest tests/test_gf_core.py -q
```

Esse arquivo está em `tests/`, que o workflow `.github/workflows/founder_panel_tests.yml` executa com `python -m pytest tests/ -q`.

## Arquitetura

```
apps/gf-core/
  core/     CNPJ, RNA Atlas, entidades, máquina de status, CSV, backup zip
  db/       schema SQLite, PRAGMA foreign_keys=ON, repositório
  api/      FastAPI + Pydantic (casca sobre o repositório)
  ui/       Streamlit: CRM, tabelas, filtros, OS, export
```

A regra de negócio mora no repositório. API e painel só chamam essa camada. Toda leitura de caixa exige `entidade`. Não existe listagem “de todas”.

Entidades de caixa: **AI** Ativos Imobiliários, **HC** Heros Custom, **FSE** Fidalgo Soluções Elétricas, **EF** Eletro Fidalgo Ltda, **PF** Posto Fidalgo / Eco Hub. Um cliente, um equipamento e uma OS nascem numa entidade e não mudam de entidade. O equipamento tem de ser do mesmo cliente.

## Schema

`PRAGMA foreign_keys=ON` em toda conexão. Arquivo `db/schema.sql`.

`clientes_b2b`: `id_cliente` PK, `entidade`, `razao_social` NOT NULL, `cnpj` UNIQUE NOT NULL, `inscricao_estadual`, `contato_responsavel`, `telefone`, `email_fiscal`, `endereco`, `observacoes`.

`equipamentos`: `id_equipamento` PK, `id_cliente` FK, `entidade`, `tipo_equipamento` NOT NULL (`Transformador` | `Motor Elétrico` | `Gerador` | `Disjuntor`), `marca_modelo`, `numero_serie` UNIQUE NOT NULL, `potencia_especificacao`, `link_pasta_drive` (nome RNA, não é URL), `status_atual` default `Diagnóstico`.

`ordens_servico`: `id_os` PK, `id_cliente` FK, `id_equipamento` FK, `entidade`, `data_abertura` NOT NULL, `data_previsao`, `data_conclusao`, `descricao_servico`, `status_os` default `Orçamento`, `valor_orcamento` e `valor_final` REAL default `0.0`, `centro_custo` default `EF-OPEX`, `responsavel_tecnico`.

A coluna `entidade` existe nas três tabelas para a segregação ser verificável no banco, não só na tela.

### OS industrial

Abertura só em `Orçamento`. Transições válidas, sem pular etapa:

`Orçamento` → `Aprovado` → `Em Manutenção` → `Teste de Carga` → `Faturado`

`Faturado` é terminal e não altera valores. `data_conclusao` é preenchida nessa passagem.

### EF-OPEX

OS da EF só existe com `centro_custo = EF-OPEX`. O default da coluna é esse código de propósito: uma OS EF sem centro explícito continua em `EF-OPEX`. Nas outras entidades o mesmo default é recusado pelo trigger, e o repositório grava o centro da própria entidade (`HC-OPEX`, `FSE-OPEX` ou `FSE-CAPEX`, `AI-OPEX`, `PF-OPEX`). `EF-OPEX` não entra em HC, FSE, AI ou PF.

## RNA Atlas

Todo arquivo ou pasta gerado pelo app segue:

`AAAAMMDD_TAG_DESCRICAO_Vxx.ext`

Exemplo válido: `20261022_EF_Laudo_Transformador_Pesa_V01.pdf`.

- Data real de calendário, tag `AI|HC|FSE|EF|PF`, descrição em tokens `Palavra` separados por `_`.
- Versão `V01`–`V99`. A próxima chamada com a mesma data, tag, descrição e extensão sobe um degrau.
- A pasta do equipamento vai sozinha para `link_pasta_drive`, no formato `AAAAMMDD_EF_Pasta_Transformador_V01.dir`. Não há upload.
- O backup é um zip (`ZIP_DEFLATED`) do sqlite inteiro, nome `AAAAMMDD_TAG_Backup_SQLite_Vxx.zip`. Backup é cópia do arquivo local para o operador. Não é relatório de caixa e não mistura entidades num CSV.

Um nome sem `_Vxx` não passa no validador.

## Contrato CSV · planilha `Grupo_Fidalgo_BI`

O export é um CSV local, UTF-8, separador vírgula, decimal com ponto e duas casas. Os cabeçalhos repetem as abas da planilha mestre para poder colar sem renomear coluna. Este app **não** lê e **não** escreve a planilha. Não copia linha de imóvel, cenário ou patrimônio.

Só entra OS em `Faturado`. Orçamento não vira receita. Cada chamada devolve **uma** entidade. `Custo_R`, `Resultado_R`, `Patrimonio_Mercado_R`, margem, vagas e NF ficam vazios: o app não apura esses números.

### Aba `3_FSE_CentrosCusto` — só EF e FSE

```
AnoMes,Entidade,CentroCusto,Descricao,Valor_R,Cliente_Projeto,NF,Observacoes
```

| Coluna | Origem |
| --- | --- |
| AnoMes | `YYYY-MM` de `data_conclusao` |
| Entidade | `EF` ou `FSE` |
| CentroCusto | vocabulário da aba: `OPEX` ou `CAPEX`. `EF-OPEX` interno vira `OPEX`. `FSE-OPEX` vira `OPEX`. `FSE-CAPEX` vira `CAPEX` |
| Descricao | `descricao_servico` |
| Valor_R | `valor_final` |
| Cliente_Projeto | `id_cliente` |
| NF | vazio |
| Observacoes | `id_os` e `centro_custo` interno. Na EF também `separar_de=FSE` |

HC, AI e PF não saem nesta aba.

### Aba `2_Heros_Operacional` — só HC

```
AnoMes,Entidade,Tipo,Categoria,Valor_R,Custo_R,Margem_R,Qtd_OS,Qtd_Vendas,Ocupacao_Vagas_pct,Vagas_Inadimplentes,Observacoes
```

Uma linha por competência: `Tipo=OS`, `Categoria=Servicos`, `Valor_R` = soma de `valor_final`, `Qtd_OS` = contagem. O resto numérico fica vazio.

### Aba `5_Grupo_Consolidado` — uma entidade por arquivo

```
AnoMes,Entidade,Receita_R,Custo_R,Resultado_R,Patrimonio_Mercado_R,Observacoes
```

`Receita_R` é a soma de `valor_final` das OS faturadas daquela entidade na competência. Custo, resultado e patrimônio ficam em branco.

## Gates

- Local, `127.0.0.1`, banco sqlite, sem deploy e sem domínio.
- Sem cliente real, sem CNPJ real, sem preço de tabela. Fixture de teste é explícita e óbvia.
- Sem segredo, sem token, sem n8n, sem Hotmart.
- Caixa e export não atravessam entidade.
- Merge fica com o Founder.
