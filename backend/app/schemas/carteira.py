from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import ObjetivoCarteira, TipoCarteira


class CarteiraBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    tipo: TipoCarteira
    objetivo: ObjetivoCarteira
    descricao: str | None = Field(None, max_length=500)
    ativa: bool = True
    saldo_inicial: Decimal = Decimal("0.00")
    saldo_atual: Decimal = Decimal("0.00")
    observacoes: str | None = None


class CarteiraCreate(CarteiraBase):
    usuario_id: UUID


class CarteiraUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=255)
    tipo: TipoCarteira | None = None
    objetivo: ObjetivoCarteira | None = None
    descricao: str | None = Field(None, max_length=500)
    ativa: bool | None = None
    saldo_inicial: Decimal | None = None
    saldo_atual: Decimal | None = None
    observacoes: str | None = None


class CarteiraRead(CarteiraBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    usuario_id: UUID
    created_at: datetime
    updated_at: datetime