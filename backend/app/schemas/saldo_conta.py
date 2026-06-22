from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.enums import TipoSaldoConta


class SaldoContaBase(BaseModel):
    conta_id: UUID
    tipo: TipoSaldoConta
    valor: Decimal = Field(..., gt=0)
    data_operacao: date
    descricao: str | None = None

    @field_validator("valor", mode="before")
    @classmethod
    def normalizar_valor(cls, v: object) -> Decimal:
        if isinstance(v, Decimal):
            return v
        return Decimal(str(v))


class SaldoContaCreate(SaldoContaBase):
    pass


class SaldoContaRead(SaldoContaBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime