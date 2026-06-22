from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.instituicao import InstituicaoCreate, InstituicaoRead, InstituicaoUpdate
from app.services.instituicao_service import InstituicaoService

router = APIRouter()


@router.post(
    "",
    response_model=InstituicaoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova instituição",
)
def create_instituicao(
    payload: InstituicaoCreate,
    db: Session = Depends(get_db),
) -> InstituicaoRead:
    service = InstituicaoService(db)
    return service.create_instituicao(payload)


@router.get(
    "",
    response_model=List[InstituicaoRead],
    summary="Lista todas as instituições",
)
def get_all_instituicoes(
    db: Session = Depends(get_db),
) -> List[InstituicaoRead]:
    service = InstituicaoService(db)
    return service.get_all_instituicoes()


@router.get(
    "/{instituicao_id}",
    response_model=InstituicaoRead,
    summary="Busca uma instituição por ID",
)
def get_instituicao_by_id(
    instituicao_id: UUID,
    db: Session = Depends(get_db),
) -> InstituicaoRead:
    service = InstituicaoService(db)
    db_instituicao = service.get_instituicao_by_id(instituicao_id)
    if db_instituicao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instituição não encontrada",
        )
    return db_instituicao


@router.put(
    "/{instituicao_id}",
    response_model=InstituicaoRead,
    summary="Atualiza uma instituição",
)
def update_instituicao(
    instituicao_id: UUID,
    payload: InstituicaoUpdate,
    db: Session = Depends(get_db),
) -> InstituicaoRead:
    service = InstituicaoService(db)
    updated_instituicao = service.update_instituicao(instituicao_id, payload)
    if updated_instituicao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instituição não encontrada",
        )
    return updated_instituicao


@router.delete(
    "/{instituicao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma instituição",
)
def delete_instituicao(
    instituicao_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    service = InstituicaoService(db)
    deleted = service.delete_instituicao(instituicao_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instituição não encontrada",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)