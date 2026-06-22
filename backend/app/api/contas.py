from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.conta import ContaCreate, ContaRead, ContaUpdate
from app.services.conta_service import ContaService

router = APIRouter()


@router.post(
    "",
    response_model=ContaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova conta",
)
def create_conta(
    payload: ContaCreate,
    db: Session = Depends(get_db),
) -> ContaRead:
    service = ContaService(db)
    return service.create_conta(payload)


@router.get(
    "",
    response_model=List[ContaRead],
    summary="Lista todas as contas",
)
def get_all_contas(
    skip: int = 0,
    limit: int = 100,
    instituicao_id: UUID | None = None,
    db: Session = Depends(get_db),
) -> List[ContaRead]:
    service = ContaService(db)
    return service.get_all_contas(skip=skip, limit=limit, instituicao_id=instituicao_id)


@router.get(
    "/{conta_id}",
    response_model=ContaRead,
    summary="Busca uma conta por ID",
)
def get_conta_by_id(
    conta_id: UUID,
    db: Session = Depends(get_db),
) -> ContaRead:
    service = ContaService(db)
    db_conta = service.get_conta_by_id(conta_id)
    if db_conta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return db_conta


@router.put(
    "/{conta_id}",
    response_model=ContaRead,
    summary="Atualiza uma conta existente",
)
def update_conta(
    conta_id: UUID,
    payload: ContaUpdate,
    db: Session = Depends(get_db),
) -> ContaRead:
    service = ContaService(db)
    updated_conta = service.update_conta(conta_id, payload)
    if updated_conta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return updated_conta


@router.delete(
    "/{conta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma conta",
)
def delete_conta(
    conta_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    service = ContaService(db)
    deleted = service.delete_conta(conta_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)