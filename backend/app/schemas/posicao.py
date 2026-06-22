from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PosicaoRead(BaseModel):
    id: UUID
    carteira_id: UUID
    conta_id: UUID
    ativo_id: UUID

    quantidade: Decimal
    preco_medio: Decimal
    custo_total: Decimal

    model_config = ConfigDict(from_attributes=True)