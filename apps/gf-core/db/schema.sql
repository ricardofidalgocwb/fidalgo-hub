-- Schema local do gf-core. Sem carga de dados.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes_b2b (
    id_cliente TEXT PRIMARY KEY,
    entidade TEXT NOT NULL CHECK (entidade IN ('EF', 'FSE', 'HC', 'AI', 'PF')),
    razao_social TEXT NOT NULL,
    cnpj TEXT UNIQUE NOT NULL,
    inscricao_estadual TEXT,
    contato_responsavel TEXT,
    telefone TEXT,
    email_fiscal TEXT,
    endereco TEXT,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS equipamentos (
    id_equipamento TEXT PRIMARY KEY,
    id_cliente TEXT NOT NULL REFERENCES clientes_b2b (id_cliente),
    entidade TEXT NOT NULL CHECK (entidade IN ('EF', 'FSE', 'HC', 'AI', 'PF')),
    tipo_equipamento TEXT NOT NULL CHECK (
        tipo_equipamento IN ('Transformador', 'Motor Elétrico', 'Gerador', 'Disjuntor')
    ),
    marca_modelo TEXT,
    numero_serie TEXT UNIQUE NOT NULL,
    potencia_especificacao TEXT,
    status_atual TEXT NOT NULL DEFAULT 'Diagnóstico'
);

CREATE TABLE IF NOT EXISTS ordens_servico (
    id_os TEXT PRIMARY KEY,
    id_cliente TEXT NOT NULL REFERENCES clientes_b2b (id_cliente),
    id_equipamento TEXT NOT NULL REFERENCES equipamentos (id_equipamento),
    entidade TEXT NOT NULL CHECK (entidade IN ('EF', 'FSE', 'HC', 'AI', 'PF')),
    data_abertura TEXT NOT NULL,
    data_previsao TEXT,
    data_conclusao TEXT,
    descricao_servico TEXT,
    status_os TEXT NOT NULL DEFAULT 'Orçamento' CHECK (
        status_os IN ('Orçamento', 'Aprovado', 'Em Manutenção', 'Teste de Carga', 'Faturado')
    ),
    valor_orcamento REAL CHECK (valor_orcamento IS NULL OR valor_orcamento > 0),
    valor_final REAL CHECK (valor_final IS NULL OR valor_final > 0),
    centro_custo TEXT NOT NULL DEFAULT 'EF-OPEX' CHECK (
        centro_custo IN (
            'AI-OPEX', 'HC-OPEX', 'FSE-OPEX', 'FSE-CAPEX', 'EF-OPEX', 'PF-OPEX'
        )
    ),
    responsavel_tecnico TEXT,
    link_pasta_drive TEXT NOT NULL,
    ref_foto_tipada TEXT
);

CREATE TABLE IF NOT EXISTS recebimentos (
    id TEXT PRIMARY KEY,
    id_os TEXT NOT NULL REFERENCES ordens_servico (id_os),
    entidade TEXT NOT NULL CHECK (entidade IN ('EF', 'FSE', 'HC', 'AI', 'PF')),
    data_recebimento TEXT NOT NULL,
    valor_recebido REAL NOT NULL CHECK (valor_recebido > 0),
    forma TEXT NOT NULL,
    obs TEXT
);

CREATE TABLE IF NOT EXISTS medicoes (
    id TEXT PRIMARY KEY,
    id_os TEXT NOT NULL REFERENCES ordens_servico (id_os),
    entidade TEXT NOT NULL CHECK (entidade IN ('EF', 'FSE', 'HC', 'AI', 'PF')),
    grandeza TEXT NOT NULL,
    valor TEXT NOT NULL,
    unidade TEXT NOT NULL,
    data TEXT NOT NULL,
    responsavel TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clientes_entidade ON clientes_b2b (entidade);
CREATE INDEX IF NOT EXISTS idx_equipamentos_entidade ON equipamentos (entidade);
CREATE INDEX IF NOT EXISTS idx_os_entidade ON ordens_servico (entidade);
CREATE INDEX IF NOT EXISTS idx_recebimentos_entidade ON recebimentos (entidade);
CREATE INDEX IF NOT EXISTS idx_medicoes_entidade ON medicoes (entidade);

CREATE TRIGGER IF NOT EXISTS trg_cli_entidade_imutavel
BEFORE UPDATE ON clientes_b2b
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'entidade do cliente e imutavel')
    WHERE NEW.entidade != OLD.entidade;
END;

CREATE TRIGGER IF NOT EXISTS trg_eq_insert
BEFORE INSERT ON equipamentos
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'equipamento.entidade diverge do cliente')
    WHERE (SELECT entidade FROM clientes_b2b WHERE id_cliente = NEW.id_cliente) IS NOT NULL
      AND (SELECT entidade FROM clientes_b2b WHERE id_cliente = NEW.id_cliente) != NEW.entidade;
END;

CREATE TRIGGER IF NOT EXISTS trg_eq_update
BEFORE UPDATE ON equipamentos
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'entidade do equipamento e imutavel')
    WHERE NEW.entidade != OLD.entidade;
    SELECT RAISE(ABORT, 'equipamento.entidade diverge do cliente')
    WHERE (SELECT entidade FROM clientes_b2b WHERE id_cliente = NEW.id_cliente) IS NOT NULL
      AND (SELECT entidade FROM clientes_b2b WHERE id_cliente = NEW.id_cliente) != NEW.entidade;
END;

CREATE TRIGGER IF NOT EXISTS trg_os_insert
BEFORE INSERT ON ordens_servico
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'OS abre em Orçamento')
    WHERE NEW.status_os != 'Orçamento';
    SELECT RAISE(ABORT, 'EF exige centro_custo EF-OPEX')
    WHERE NEW.entidade = 'EF' AND NEW.centro_custo != 'EF-OPEX';
    SELECT RAISE(ABORT, 'EF-OPEX exclusivo da entidade EF')
    WHERE NEW.entidade != 'EF' AND NEW.centro_custo = 'EF-OPEX';
    SELECT RAISE(ABORT, 'centro_custo incompativel com a entidade')
    WHERE (NEW.entidade = 'AI' AND NEW.centro_custo != 'AI-OPEX')
       OR (NEW.entidade = 'HC' AND NEW.centro_custo != 'HC-OPEX')
       OR (NEW.entidade = 'PF' AND NEW.centro_custo != 'PF-OPEX')
       OR (NEW.entidade = 'FSE' AND NEW.centro_custo NOT IN ('FSE-OPEX', 'FSE-CAPEX'));
    SELECT RAISE(ABORT, 'OS.entidade diverge do cliente')
    WHERE (SELECT entidade FROM clientes_b2b WHERE id_cliente = NEW.id_cliente) IS NOT NULL
      AND (SELECT entidade FROM clientes_b2b WHERE id_cliente = NEW.id_cliente) != NEW.entidade;
    SELECT RAISE(ABORT, 'OS.entidade diverge do equipamento')
    WHERE (SELECT entidade FROM equipamentos WHERE id_equipamento = NEW.id_equipamento) IS NOT NULL
      AND (SELECT entidade FROM equipamentos WHERE id_equipamento = NEW.id_equipamento) != NEW.entidade;
    SELECT RAISE(ABORT, 'equipamento nao pertence ao cliente')
    WHERE (SELECT id_cliente FROM equipamentos WHERE id_equipamento = NEW.id_equipamento) IS NOT NULL
      AND (SELECT id_cliente FROM equipamentos WHERE id_equipamento = NEW.id_equipamento) != NEW.id_cliente;
END;

CREATE TRIGGER IF NOT EXISTS trg_os_update
BEFORE UPDATE ON ordens_servico
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'entidade da OS e imutavel')
    WHERE NEW.entidade != OLD.entidade;
    SELECT RAISE(ABORT, 'transicao de status invalida')
    WHERE NEW.status_os != OLD.status_os
      AND NOT (
          (OLD.status_os = 'Orçamento' AND NEW.status_os = 'Aprovado')
          OR (OLD.status_os = 'Aprovado' AND NEW.status_os = 'Em Manutenção')
          OR (OLD.status_os = 'Em Manutenção' AND NEW.status_os = 'Teste de Carga')
          OR (OLD.status_os = 'Teste de Carga' AND NEW.status_os = 'Faturado')
      );
    SELECT RAISE(ABORT, 'Teste de Carga exige medicao e foto tipada')
    WHERE NEW.status_os != OLD.status_os
      AND NEW.status_os IN ('Teste de Carga', 'Faturado')
      AND (
          NEW.ref_foto_tipada IS NULL
          OR TRIM(NEW.ref_foto_tipada) = ''
          OR NOT EXISTS (
              SELECT 1 FROM medicoes
              WHERE id_os = NEW.id_os AND entidade = NEW.entidade
          )
      );
    SELECT RAISE(ABORT, 'EF exige centro_custo EF-OPEX')
    WHERE NEW.entidade = 'EF' AND NEW.centro_custo != 'EF-OPEX';
    SELECT RAISE(ABORT, 'EF-OPEX exclusivo da entidade EF')
    WHERE NEW.entidade != 'EF' AND NEW.centro_custo = 'EF-OPEX';
    SELECT RAISE(ABORT, 'OS faturada nao altera valores')
    WHERE OLD.status_os = 'Faturado'
      AND (
          NEW.valor_final IS NOT OLD.valor_final
          OR NEW.valor_orcamento IS NOT OLD.valor_orcamento
      );
END;

CREATE TRIGGER IF NOT EXISTS trg_rec_insert
BEFORE INSERT ON recebimentos
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'recebimento.entidade diverge da OS')
    WHERE (SELECT entidade FROM ordens_servico WHERE id_os = NEW.id_os) IS NOT NULL
      AND (SELECT entidade FROM ordens_servico WHERE id_os = NEW.id_os) != NEW.entidade;
END;

CREATE TRIGGER IF NOT EXISTS trg_rec_update
BEFORE UPDATE ON recebimentos
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'entidade do recebimento e imutavel')
    WHERE NEW.entidade != OLD.entidade;
END;

CREATE TRIGGER IF NOT EXISTS trg_med_insert
BEFORE INSERT ON medicoes
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'medicao.entidade diverge da OS')
    WHERE (SELECT entidade FROM ordens_servico WHERE id_os = NEW.id_os) IS NOT NULL
      AND (SELECT entidade FROM ordens_servico WHERE id_os = NEW.id_os) != NEW.entidade;
END;

CREATE TRIGGER IF NOT EXISTS trg_med_update
BEFORE UPDATE ON medicoes
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'entidade da medicao e imutavel')
    WHERE NEW.entidade != OLD.entidade;
END;
