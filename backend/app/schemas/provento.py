# FILE: app/schemas/provento.py
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict # Importar ConfigDict

from app.schemas.enums import TipoProvento # Importação adicionada

class ProventoBase(BaseModel):
    ativo_id: UUID
    tipo: TipoProvento = Field(
        ...,
        description="DIVIDENDO, JCP, RENDIMENTO ou AMORTIZACAO",
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
    model_config = ConfigDict(from_attributes=True) # Usando ConfigDict para Pydantic v2+

    id: UUID = Field(..., description="ID único do provento")
    ativo_id: UUID
    tipo: TipoProvento
    valor_bruto: Decimal
    ir_retido: Decimal
    valor_liquido: Decimal # Este campo será populado pelo serviço/ORM
    data_com: date
    data_ex: date
    data_pagamento: date
    quantidade_na_data: Decimal
    reinvestido: bool
    created_at: datetime = Field(..., description="Data e hora de criação do registro") # Corrigido para não opcional
    updated_at: datetime = Field(..., description="Data e hora da última atualização do registro") # Adicionado para consistência