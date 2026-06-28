# FILE: backend/app/api/carteiras.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.database import get_db
from app.schemas.carteira import CarteiraCreate, CarteiraRead, CarteiraUpdate
from app.services import carteira_service

router = APIRouter()

@router.post(
    "",
    response_model=CarteiraRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova carteira para o usuário autenticado",
)
def create_carteira_endpoint(
    carteira: CarteiraCreate,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> CarteiraRead:
    return carteira_service.create_carteira(
        db=db,
        carteira=carteira,
        usuario_id=current_user.id,
    )

@router.get(
    "",
    response_model=List[CarteiraRead],
    summary="Lista carteiras do usuário autenticado",
)
def read_carteiras_endpoint(
    current_user: CurrentUser, # CORRIGIDO: Movido para antes dos argumentos com Query
    db: Session = Depends(get_db), # CORRIGIDO: Movido para antes dos argumentos com Query
    skip: int = 0,
    limit: int = 100,
) -> List[CarteiraRead]:
    return carteira_service.get_carteiras(
        db=db,
        usuario_id=current_user.id,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/{carteira_id}",
    response_model=CarteiraRead,
    summary="Busca uma carteira por ID (somente do usuário autenticado)",
)
def read_carteira_endpoint(
    carteira_id: UUID,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> CarteiraRead:
    db_carteira = carteira_service.get_carteira(
        db=db,
        carteira_id=carteira_id,
        usuario_id=current_user.id,
    )
    if db_carteira is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carteira não encontrada",
        )
    return db_carteira

@router.put(
    "/{carteira_id}",
    response_model=CarteiraRead,
    summary="Atualiza uma carteira do usuário autenticado",
)
def update_carteira_endpoint(
    carteira_id: UUID,
    carteira: CarteiraUpdate,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> CarteiraRead:
    db_carteira = carteira_service.update_carteira(
        db=db,
        carteira_id=carteira_id,
        carteira=carteira,
        usuario_id=current_user.id,
    )
    if db_carteira is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carteira não encontrada",
        )
    return db_carteira

@router.delete(
    "/{carteira_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma carteira do usuário autenticado",
)
def delete_carteira_endpoint(
    carteira_id: UUID,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> Response:
    deleted = carteira_service.delete_carteira(
        db=db,
        carteira_id=carteira_id,
        usuario_id=current_user.id,
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carteira não encontrada",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)