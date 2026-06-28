# FILE: backend/app/schemas/provento.py
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from app.schemas.enums import TipoProvento

class ProventoBase(BaseModel):
    carteira_id: UUID = Field(..., description="Carteira que recebe o provento") # Tornar obrigatório
    conta_id: Optional[UUID] = Field(
        None,
        description="Conta de liquidação do provento (opcional)",
    )
    ativo_id: UUID
    tipo: TipoProvento = Field(
        ...,
        description="DIVIDENDO, JCP, RENDIMENTO, AMORTIZACAO ou OUTRO",
    )
    valor_bruto: Decimal = Field(..., gt=0, decimal_places=8, description="Valor bruto do provento")
    ir_retido: Decimal = Field(Decimal("0.00"), ge=0, decimal_places=8, description="Imposto de renda retido na fonte")
    data_com: date = Field(..., description="Data 'com' do provento")
    data_ex: Optional[date] = Field(None, description="Data 'ex' do provento")
    data_pagamento: date = Field(..., description="Data de pagamento do provento")
    quantidade_na_data: Decimal = Field(
        ...,
        gt=0,
        decimal_places=8,
        description="Quantidade em posição na data-com",
    )
    reinvestido: bool = False
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações adicionais sobre o provento")

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

    @model_validator(mode="after")
    def calculate_liquid_value(self) -> "ProventoBase":
        if self.valor_bruto is not None and self.ir_retido is not None:
            if self.ir_retido > self.valor_bruto:
                raise ValueError("IR retido não pode ser maior que o valor bruto do provento.")
        return self

class ProventoCreate(ProventoBase):
    pass

class ProventoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    carteira_id: UUID
    # conta_id: Optional[UUID] # Removido, pois não está no modelo Provento
    ativo_id: UUID
    tipo: TipoProvento
    valor_bruto: Decimal
    ir_retido: Decimal
    valor_liquido: Decimal
    data_com: date
    data_ex: Optional[date]
    data_pagamento: date
    quantidade_na_data: Decimal
    reinvestido: bool
    observacoes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
