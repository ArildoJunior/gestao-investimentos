from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ProventoBase(BaseModel):
    ativo_id: UUID
    tipo: str = Field(
        ...,
        description="DIVIDENDO, JCP, RENDIMENTO ou AMORTIZACAO",
        pattern=r"^(DIVIDENDO|JCP|RENDIMENTO|AMORTIZACAO)$",
    )
    valor_bruto: Decimal = Field(..., gt=0)
    ir_retido: Decimal = Field(default=Decimal("0"))
    data_com: date
    data_ex: date
    data_pagamento: date
    quantidade_na_data: Decimal = Field(..., gt=0)
    reinvestido: bool = False

    @field_validator("valor_bruto", "ir_retido", "quantidade_na_data", mode="before")
    def normalizar_decimal(cls, v):
        if v is None:
            return Decimal("0")
        if isinstance(v, Decimal):
            return v
        try:
            return Decimal(str(v))
        except Exception as e:
            raise ValueError(f"Valor numérico inválido: {v}") from e

    @property
    def valor_liquido_calculado(self) -> Decimal:
        return self.valor_bruto - self.ir_retido


class ProventoCreate(ProventoBase):
    """
    Payload de criação de provento.
    valor_liquido será calculado na camada de serviço.
    """
    pass


class ProventoRead(BaseModel):
    id: UUID
    ativo_id: UUID
    tipo: str
    valor_bruto: Decimal
    ir_retido: Decimal
    valor_liquido: Decimal
    data_com: date
    data_ex: date
    data_pagamento: date
    quantidade_na_data: Decimal
    reinvestido: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True