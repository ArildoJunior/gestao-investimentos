from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PosicaoRead(BaseModel):
    id: UUID
    carteira_id: UUID
    conta_id: UUID | None
    ativo_id: UUID

    quantidade: Decimal
    preco_medio: Decimal
    custo_total: Decimal

    class Config:
        from_attributes = True