from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.carteira import CarteiraCreate, CarteiraRead, CarteiraUpdate
from app.services import carteira_service

router = APIRouter()


@router.post(
    "",
    response_model=CarteiraRead,
    status_code=status.HTTP_201_CREATED,
)
def create_carteira_endpoint(
    carteira: CarteiraCreate,
    db: Session = Depends(get_db),
) -> CarteiraRead:
    return carteira_service.create_carteira(db=db, carteira=carteira)


@router.get(
    "",
    response_model=List[CarteiraRead],
)
def read_carteiras_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[CarteiraRead]:
    return carteira_service.get_carteiras(db, skip=skip, limit=limit)


@router.get(
    "/{carteira_id}",
    response_model=CarteiraRead,
)
def read_carteira_endpoint(
    carteira_id: UUID,
    db: Session = Depends(get_db),
) -> CarteiraRead:
    db_carteira = carteira_service.get_carteira(db, carteira_id=carteira_id)
    if db_carteira is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    return db_carteira


@router.put(
    "/{carteira_id}",
    response_model=CarteiraRead,
)
def update_carteira_endpoint(
    carteira_id: UUID,
    carteira: CarteiraUpdate,
    db: Session = Depends(get_db),
) -> CarteiraRead:
    db_carteira = carteira_service.update_carteira(db, carteira_id, carteira)
    if db_carteira is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    return db_carteira


@router.delete(
    "/{carteira_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_carteira_endpoint(
    carteira_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    db_carteira = carteira_service.delete_carteira(db, carteira_id)
    if db_carteira is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)