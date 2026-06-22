from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import ObjetivoCarteira, TipoCarteira


class CarteiraBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=80, description="Nome da carteira")
    tipo: TipoCarteira = Field(..., description="Tipo da carteira")
    objetivo: ObjetivoCarteira = Field(..., description="Objetivo da carteira")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição detalhada")
    ativa: bool = Field(True, description="Indica se a carteira está ativa")
    saldo_inicial: Decimal = Field(Decimal("0.00"), ge=0, description="Saldo inicial")
    saldo_atual: Decimal = Field(Decimal("0.00"), ge=0, description="Saldo atual")
    observacoes: Optional[str] = Field(None, description="Observações")


class CarteiraCreate(CarteiraBase):
    usuario_id: UUID = Field(..., description="ID do usuário dono da carteira")


class CarteiraUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=80)
    tipo: Optional[TipoCarteira] = None
    objetivo: Optional[ObjetivoCarteira] = None
    descricao: Optional[str] = Field(None, max_length=500)
    ativa: Optional[bool] = None
    saldo_inicial: Optional[Decimal] = Field(None, ge=0)
    saldo_atual: Optional[Decimal] = Field(None, ge=0)
    observacoes: Optional[str] = None


class CarteiraRead(CarteiraBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    usuario_id: UUID
    created_at: datetime
    updated_at: datetime