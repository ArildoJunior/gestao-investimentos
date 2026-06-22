from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.enums import TipoProvento


class ProventoBase(BaseModel):
    carteira_id: Optional[UUID] = Field(
        None, description="Carteira que recebe o provento"
    )
    conta_id: Optional[UUID] = Field(
        None,
        description="Conta de liquidação do provento (opcional)",
    )
    ativo_id: UUID
    tipo: TipoProvento = Field(
        ...,
        description="DIVIDENDO, JCP, RENDIMENTO, AMORTIZACAO ou OUTRO",
    )
    valor_bruto: Decimal = Field(..., gt=0)
    data_com: date
    data_pagamento: date
    quantidade: Decimal = Field(
        ...,
        gt=0,
        description="Quantidade em posição na data-com",
    )
    reinvestido: bool = False
    observacoes: Optional[str] = None

    @field_validator("valor_bruto", "quantidade", mode="before")
    def normalizar_decimal(cls, v):
        if v is None:
            return Decimal("0")
        if isinstance(v, Decimal):
            return v
        try:
            return Decimal(str(v))
        except Exception as e:
            raise ValueError(f"Valor numérico inválido: {v}") from e


class ProventoCreate(ProventoBase):
    pass


class ProventoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    carteira_id: UUID
    conta_id: Optional[UUID]
    ativo_id: UUID
    tipo: TipoProvento
    valor_bruto: Decimal
    valor_liquido: Decimal
    data_com: date
    data_pagamento: date
    quantidade: Decimal
    reinvestido: bool
    observacoes: Optional[str] = None
    created_at: datetime
    updated_at: datetime