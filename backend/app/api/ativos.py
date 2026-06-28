# FILE: backend/app/api/ativos.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser # Corrigido para app.api.dependencies
from app.database import get_db
from app.schemas.ativo import AtivoCreate, AtivoRead, AtivoUpdate
from app.services.ativo_service import AtivoService

router = APIRouter()

# Ativos são cadastros globais de mercado — qualquer usuário autenticado
# pode ler e criar. Não há isolamento por usuario_id aqui porque
# PETR4 é a mesma PETR4 para todos os usuários.
# O isolamento ocorre nas posições, movimentações e carteiras.

@router.post(
    "",
    response_model=AtivoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo ativo",
)
def create_ativo(
    payload: AtivoCreate,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> AtivoRead:
    service = AtivoService(db)
    return service.create_ativo(payload)

@router.get(
    "",
    response_model=List[AtivoRead],
    summary="Lista todos os ativos",
)
def get_all_ativos(
    current_user: CurrentUser, # CORRIGIDO: Movido para antes dos argumentos com Query
    db: Session = Depends(get_db), # CORRIGIDO: Movido para antes dos argumentos com Query
    skip: int = 0,
    limit: int = 100,
) -> List[AtivoRead]:
    service = AtivoService(db)
    return service.get_all_ativos(skip=skip, limit=limit)

@router.get(
    "/{ativo_id}",
    response_model=AtivoRead,
    summary="Busca um ativo por ID",
)
def get_ativo_by_id(
    ativo_id: UUID,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> AtivoRead:
    service = AtivoService(db)
    db_ativo = service.get_ativo_by_id(ativo_id)
    if db_ativo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ativo não encontrado",
        )
    return db_ativo

@router.put(
    "/{ativo_id}",
    response_model=AtivoRead,
    summary="Atualiza um ativo existente",
)
def update_ativo(
    ativo_id: UUID,
    payload: AtivoUpdate,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> AtivoRead:
    service = AtivoService(db)
    updated = service.update_ativo(ativo_id, payload)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ativo não encontrado",
        )
    return updated

@router.delete(
    "/{ativo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um ativo",
)
def delete_ativo(
    ativo_id: UUID,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> Response:
    service = AtivoService(db)
    deleted = service.delete_ativo(ativo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ativo não encontrado",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)