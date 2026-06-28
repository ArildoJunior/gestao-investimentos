# FILE: backend/app/api/radar_dividendos.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser
from app.database import get_db
from app.schemas.radar_dividendos import RadarDividendosItem, RadarDividendosFiltro
from app.services.radar_dividendos_service import (
    listar_radar_dividendos,
    listar_historico_proventos,
)

router = APIRouter()


@router.get(
    "",
    response_model=List[RadarDividendosItem],
    summary="Proventos com pagamento nos próximos N dias",
)
def get_radar_dividendos(
    dias: int = Query(90, ge=1, le=365),
    carteira_id: UUID | None = Query(None),
    ativo_id: UUID | None = Query(None),
    apenas_nao_reinvestidos: bool = Query(False),
    current_user=Depends(CurrentUser),
    db: Session = Depends(get_db),
) -> List[RadarDividendosItem]:
    filtro = RadarDividendosFiltro(
        dias=dias,
        carteira_id=carteira_id,
        ativo_id=ativo_id,
        apenas_nao_reinvestidos=apenas_nao_reinvestidos,
    )
    return listar_radar_dividendos(db, usuario_id=current_user.id, filtro=filtro)


@router.get(
    "/historico",
    response_model=List[RadarDividendosItem],
    summary="Histórico completo de proventos recebidos",
)
def get_historico_proventos(
    carteira_id: UUID | None = Query(None),
    ativo_id: UUID | None = Query(None),
    current_user=Depends(CurrentUser),
    db: Session = Depends(get_db),
) -> List[RadarDividendosItem]:
    return listar_historico_proventos(
        db,
        usuario_id=current_user.id,
        carteira_id=carteira_id,
        ativo_id=ativo_id,
    )