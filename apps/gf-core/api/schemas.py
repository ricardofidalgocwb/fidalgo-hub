"""Contratos de entrada da API local."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Entidade = Literal["AI", "HC", "FSE", "EF", "PF"]
TipoEquipamento = Literal["Transformador", "Motor Elétrico", "Gerador", "Disjuntor"]
StatusOs = Literal["Orçamento", "Aprovado", "Em Manutenção", "Teste de Carga", "Faturado"]


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ClienteIn(_Base):
    entidade: Entidade
    razao_social: str = Field(min_length=1)
    cnpj: str = Field(min_length=1)
    inscricao_estadual: str | None = None
    contato_responsavel: str | None = None
    telefone: str | None = None
    email_fiscal: str | None = None
    endereco: str | None = None
    observacoes: str | None = None


class EquipamentoIn(_Base):
    entidade: Entidade
    id_cliente: str = Field(min_length=1)
    tipo_equipamento: TipoEquipamento
    numero_serie: str = Field(min_length=1)
    marca_modelo: str | None = None
    potencia_especificacao: str | None = None
    data_referencia: date | None = None


class OsIn(_Base):
    entidade: Entidade
    id_cliente: str = Field(min_length=1)
    id_equipamento: str = Field(min_length=1)
    data_abertura: date
    descricao_servico: str | None = None
    data_previsao: date | None = None
    valor_orcamento: float = 0.0
    valor_final: float = 0.0
    centro_custo: str | None = None
    responsavel_tecnico: str | None = None


class TransicaoIn(_Base):
    status_destino: StatusOs
    quando: date | None = None


class BackupIn(_Base):
    tag: Entidade
    quando: date | None = None
