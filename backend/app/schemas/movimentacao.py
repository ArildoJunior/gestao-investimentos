from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class MovimentacaoBase(BaseModel):
    carteira_id: UUID
    conta_id: UUID | None = None
    ativo_id: UUID

    tipo_movimentacao: str = Field(..., pattern="^(COMPRA|VENDA)$")
    tipo_operacao: str = Field(
        ...,
        pattern="^(SWING_TRADE|DAY_TRADE|POSITION|OUTRO)$",
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
    pass


class MovimentacaoRead(MovimentacaoBase):
    id: UUID
    valor_bruto: Decimal
    valor_liquido: Decimal

    class Config:
        from_attributes = True