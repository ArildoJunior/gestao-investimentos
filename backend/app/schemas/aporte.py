from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.enums import OrigemAporte, TipoAporte


class AporteBase(BaseModel):
    carteira_id: UUID
    conta_id: UUID | None = None
    tipo: TipoAporte
    origem: OrigemAporte | None = None
    valor: Decimal = Field(..., gt=0)
    data_aporte: date
    movimentacao_id: UUID | None = None
    provento_id: UUID | None = None
    observacao: str | None = Field(None, max_length=500)

    @field_validator("valor", mode="before")
    @classmethod
    def normalizar_valor(cls, v: object) -> Decimal:
        if isinstance(v, Decimal):
            return v
        return Decimal(str(v))


class AporteCreate(AporteBase):
    pass


class AporteUpdate(BaseModel):
    carteira_id: UUID | None = None
    conta_id: UUID | None = None
    tipo: TipoAporte | None = None
    origem: OrigemAporte | None = None
    valor: Decimal | None = Field(None, gt=0)
    data_aporte: date | None = None
    movimentacao_id: UUID | None = None
    provento_id: UUID | None = None
    observacao: str | None = Field(None, max_length=500)

    @field_validator("valor", mode="before")
    @classmethod
    def normalizar_valor(cls, v: object) -> Decimal | None:
        if v is None:
            return None
        if isinstance(v, Decimal):
            return v
        return Decimal(str(v))


class AporteRead(AporteBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime