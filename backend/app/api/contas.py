# FILE: backend/app/api/contas.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser
from app.database import get_db
from app.schemas.conta import ContaCreate, ContaRead, ContaUpdate
from app.services.conta_service import ContaService

router = APIRouter()

@router.post(
    "",
    response_model=ContaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova conta para o usuário autenticado",
)
def create_conta(
    payload: ContaCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> ContaRead:
    service = ContaService(db)
    return service.create_conta(payload, usuario_id=current_user.id)

@router.get(
    "",
    response_model=List[ContaRead],
    summary="Lista todas as contas do usuário autenticado",
)
def get_all_contas(
    current_user: CurrentUser, # Argumento sem valor padrão (dependência)
    db: Session = Depends(get_db), # Argumento com valor padrão (dependência)
    skip: int = 0, # Argumento com valor padrão
    limit: int = 100, # Argumento com valor padrão
) -> List[ContaRead]:
    service = ContaService(db)
    return service.get_all_contas(usuario_id=current_user.id, skip=skip, limit=limit)

@router.get(
    "/{conta_id}",
    response_model=ContaRead,
    summary="Busca uma conta por ID do usuário autenticado",
)
def get_conta_by_id(
    conta_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> ContaRead:
    service = ContaService(db)
    db_conta = service.get_conta_by_id(conta_id, usuario_id=current_user.id)
    if db_conta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return db_conta

@router.put(
    "/{conta_id}",
    response_model=ContaRead,
    summary="Atualiza uma conta existente do usuário autenticado",
)
def update_conta(
    conta_id: UUID,
    payload: ContaUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> ContaRead:
    service = ContaService(db)
    updated = service.update_conta(conta_id, payload, usuario_id=current_user.id)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return updated

@router.delete(
    "/{conta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma conta do usuário autenticado",
)
def delete_conta(
    conta_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> Response:
    service = ContaService(db)
    deleted = service.delete_conta(conta_id, usuario_id=current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)