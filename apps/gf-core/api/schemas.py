"""Contratos de entrada da API local."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Entidade = Literal["EF", "FSE", "HC", "AI", "PF"]
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


class OsIn(_Base):
    entidade: Entidade
    id_cliente: str = Field(min_length=1)
    id_equipamento: str = Field(min_length=1)
    data_abertura: date
    descricao_servico: str | None = None
    data_previsao: date | None = None
    valor_orcamento: float | None = None
    valor_final: float | None = None
    centro_custo: str | None = None
    responsavel_tecnico: str | None = None
    data_referencia: date | None = None


class TransicaoIn(_Base):
    status_destino: StatusOs
    quando: date | None = None


class BackupIn(_Base):
    tag: Entidade
    quando: date | None = None


class MedicaoIn(_Base):
    entidade: Entidade
    id_os: str = Field(min_length=1)
    grandeza: str = Field(min_length=1)
    valor: str = Field(min_length=1)
    unidade: str = Field(min_length=1)
    data: date
    responsavel: str = Field(min_length=1)


class FotoTipadaIn(_Base):
    referencia: str = Field(min_length=1)


class RecebimentoIn(_Base):
    entidade: Entidade
    id_os: str = Field(min_length=1)
    data_recebimento: date
    valor_recebido: float
    forma: str = Field(min_length=1)
    obs: str | None = None
