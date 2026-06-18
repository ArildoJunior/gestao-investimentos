from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.aporte import AporteCreate, AporteRead
from app.services.aporte_service import (
    registrar_aporte,
    listar_aportes_por_carteira,
)

router = APIRouter(
    prefix="/aportes",
    tags=["aportes"],
)


@router.post(
    "/",
    response_model=AporteRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_aporte(
    payload: AporteCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um novo aporte (externo ou reinvestimento).
    """
    try:
        return registrar_aporte(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[AporteRead],
)
def listar_aportes(
    carteira_id: UUID = Query(...),
    conta_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista aportes por carteira e, opcionalmente, por conta.
    """
    return listar_aportes_por_carteira(db, carteira_id, conta_id)