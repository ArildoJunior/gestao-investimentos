# FILE: backend/app/api/radar_dividendos.py

from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.provento import Provento
from app.schemas.enums import TipoProvento

router = APIRouter()


class RadarDividendosItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ativo_id: UUID
    ticker: str
    carteira_id: UUID
    tipo: TipoProvento
    data_com: date
    data_pagamento: date
    valor_bruto: Decimal
    valor_liquido: Decimal
    quantidade: Decimal
    valor_por_cota: Decimal
    reinvestido: bool


@router.get("/", response_model=List[RadarDividendosItem])
def listar_radar_dividendos(
    dias: int = Query(90, ge=1, le=365, description="Proventos com pagamento nos próximos N dias"),
    ativo_id: Optional[UUID] = Query(None, description="Filtrar por ativo específico"),
    db: Session = Depends(get_db),
):
    """
    Retorna os proventos com data_pagamento entre hoje e hoje + N dias,
    ordenados por data_pagamento crescente.
    """
    hoje = date.today()
    ate = hoje + timedelta(days=dias)

    query = (
        db.query(Provento)
        .options(joinedload(Provento.ativo))
        .filter(
            Provento.data_pagamento >= hoje,
            Provento.data_pagamento <= ate,
        )
    )

    if ativo_id:
        query = query.filter(Provento.ativo_id == ativo_id)

    proventos = query.order_by(Provento.data_pagamento.asc()).all()

    resultado = []
    for p in proventos:
        valor_por_cota = (
            p.valor_bruto / p.quantidade
            if p.quantidade and p.quantidade > 0
            else Decimal("0")
        )
        resultado.append(
            RadarDividendosItem(
                id=p.id,
                ativo_id=p.ativo_id,
                ticker=p.ativo.ticker if p.ativo else str(p.ativo_id),
                carteira_id=p.carteira_id,
                tipo=p.tipo,
                data_com=p.data_com,
                data_pagamento=p.data_pagamento,
                valor_bruto=p.valor_bruto,
                valor_liquido=p.valor_liquido,
                quantidade=p.quantidade,
                valor_por_cota=valor_por_cota,
                reinvestido=p.reinvestido,
            )
        )

    return resultado