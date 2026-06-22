from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import Moeda, StatusConta, TipoConta


class ContaBase(BaseModel):
    instituicao_id: UUID = Field(..., description="ID da instituição à qual a conta pertence")
    nome: str = Field(..., min_length=1, max_length=255, description="Nome da conta")
    tipo: TipoConta = Field(..., description="Tipo da conta")
    moeda: Moeda = Field(Moeda.BRL, description="Moeda da conta")

    saldo_inicial: Decimal = Field(Decimal("0.00"), ge=0, description="Saldo inicial da conta")
    saldo_atual: Decimal = Field(Decimal("0.00"), ge=0, description="Saldo atual da conta")
    data_abertura: date = Field(..., description="Data de abertura da conta")

    status: StatusConta = Field(StatusConta.ATIVA, description="Status da conta")


class ContaCreate(ContaBase):
    pass


class ContaUpdate(BaseModel):
    instituicao_id: Optional[UUID] = None
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    tipo: Optional[TipoConta] = None
    moeda: Optional[Moeda] = None

    saldo_inicial: Optional[Decimal] = Field(None, ge=0)
    saldo_atual: Optional[Decimal] = Field(None, ge=0)
    data_abertura: Optional[date] = None

    status: Optional[StatusConta] = None


class ContaRead(ContaBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime