from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator, ConfigDict

from app.models.movimentacao import TipoMovimentacao, TipoOperacao


class MovimentacaoBase(BaseModel):
    carteira_id: UUID
    conta_id: UUID | None = None
    ativo_id: UUID

    tipo_movimentacao: str = Field(..., pattern="^(COMPRA|VENDA)$")
    tipo_operacao: str = Field(
        ...,
        pattern="^(SWING|SWING_TRADE|DAY_TRADE|POSITION|OUTRO)$",
    )

    data_operacao: date
    data_liquidacao: date

    quantidade: Decimal = Field(gt=0)
    preco_unitario: Decimal = Field(gt=0)

    corretagem: Decimal = Field(default=Decimal("0"))
    emolumentos: Decimal = Field(default=Decimal("0"))
    iss: Decimal = Field(default=Decimal("0"))
    outras_taxas: Decimal = Field(default=Decimal("0"))

    observacoes: str | None = None

    @field_validator("tipo_movimentacao", mode="before")
    @classmethod
    def _normalizar_tipo_movimentacao(cls, v: object) -> str:
        if v is None:
            raise ValueError("tipo_movimentacao é obrigatório.")
        valor = str(v).strip().upper()
        if valor not in {"COMPRA", "VENDA"}:
            raise ValueError("tipo_movimentacao inválido. Use COMPRA ou VENDA.")
        return valor

    @field_validator("tipo_operacao", mode="before")
    @classmethod
    def _normalizar_tipo_operacao(cls, v: object) -> str:
        if v is None:
            raise ValueError("tipo_operacao é obrigatório.")
        valor = str(v).strip().upper()
        if valor == "SWING_TRADE":
            return "SWING"
        if valor not in {"SWING", "DAY_TRADE", "POSITION", "OUTRO"}:
            raise ValueError(
                "tipo_operacao inválido. Use SWING, DAY_TRADE, POSITION ou OUTRO."
            )
        return valor

    @field_validator(
        "corretagem",
        "emolumentos",
        "iss",
        "outras_taxas",
        mode="before",
    )
    @classmethod
    def _padrao_decimal(cls, v: object, info: ValidationInfo) -> Decimal:
        if v is None:
            return Decimal("0")
        if isinstance(v, Decimal):
            return v
        return Decimal(str(v))


class MovimentacaoCreate(MovimentacaoBase):
    """
    Usada na entrada da API (/POST).
    """
    pass


class MovimentacaoRead(BaseModel):
    """
    Usada na saída da API (/POST, /GET).
    Lê diretamente do ORM Movimentacao.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    carteira_id: UUID
    conta_id: UUID | None
    ativo_id: UUID

    tipo_movimentacao: str
    tipo_operacao: str

    data_operacao: date
    data_liquidacao: date

    quantidade: Decimal
    preco_unitario: Decimal

    corretagem: Decimal
    emolumentos: Decimal
    iss: Decimal
    outras_taxas: Decimal

    valor_bruto: Decimal
    valor_liquido: Decimal

    observacoes: str | None = None

    @field_validator("tipo_movimentacao", mode="before")
    @classmethod
    def _coerce_tipo_movimentacao(cls, v):
        if isinstance(v, TipoMovimentacao):
            return v.value
        return v

    @field_validator("tipo_operacao", mode="before")
    @classmethod
    def _coerce_tipo_operacao(cls, v):
        if isinstance(v, TipoOperacao):
            return v.value
        return v