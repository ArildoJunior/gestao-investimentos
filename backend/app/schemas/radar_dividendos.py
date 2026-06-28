# FILE: backend/app/schemas/radar_dividendos.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field

from app.schemas.enums import TipoProvento


class RadarDividendosItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ativo_id: UUID
    ticker: str
    carteira_id: UUID
    tipo: TipoProvento
    data_com: date | None
    data_ex: date | None
    data_pagamento: date
    valor_bruto: Decimal
    valor_liquido: Decimal
    quantidade: Decimal
    reinvestido: bool

    @computed_field
    @property
    def valor_por_cota(self) -> Decimal:
        if self.quantidade and self.quantidade > 0:
            return (self.valor_bruto / self.quantidade).quantize(
                Decimal("0.00000001")
            )
        return Decimal("0")

    @computed_field
    @property
    def total_bruto_recebido(self) -> Decimal:
        return (self.valor_bruto * self.quantidade).quantize(Decimal("0.01"))


class RadarDividendosFiltro(BaseModel):
    """Parâmetros de filtro para o radar."""

    carteira_id: UUID | None = None
    ativo_id: UUID | None = None
    dias: int = 90
    apenas_nao_reinvestidos: bool = False