"""Erros de domínio. Mensagens curtas, sem vazar linha de outra entidade."""

from __future__ import annotations


class GfCoreError(Exception):
    """Base dos erros tratados pela API e pelo painel."""


class ValidationError(GfCoreError):
    """Campo ou formato recusado."""


class CnpjError(ValidationError):
    """CNPJ vazio, malformado ou com dígito inválido."""


class RnaAtlasError(ValidationError):
    """Nome fora do padrão RNA Atlas."""


class TransitionError(GfCoreError):
    """Mudança de status da OS que a máquina não permite."""


class EntityIsolationError(GfCoreError):
    """Tentativa de misturar caixa, centro ou entidade."""


class IntegrityFailure(GfCoreError):
    """Quebra de chave, unicidade ou vínculo."""


class NotFoundError(GfCoreError):
    """Registro ausente no recorte da entidade pedida."""
