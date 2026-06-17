from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.posicao import PosicaoRead
from app.services.posicao_service import listar_posicoes_por_carteira

router = APIRouter(prefix="/posicoes", tags=["posicoes"])


@router.get("/", response_model=list[PosicaoRead])
def listar_posicoes(
    carteira_id: UUID = Query(...),
    conta_id: UUID | None = Query(None),
    db: Session = Depends(get_db),
) -> list[PosicaoRead]:
    return listar_posicoes_por_carteira(db, carteira_id, conta_id)