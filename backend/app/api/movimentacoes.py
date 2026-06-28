# FILE: backend/app/api/movimentacoes.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.database import get_db
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoRead
from app.services.movimentacao_service import (
    listar_movimentacoes_por_carteira,
    registrar_movimentacao,
)

router = APIRouter()

@router.post(
    "",
    response_model=MovimentacaoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra uma nova movimentação (compra/venda)",
)
def criar_movimentacao(
    payload: MovimentacaoCreate,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> MovimentacaoRead:
    try:
        return registrar_movimentacao(db, payload, usuario_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.get(
    "",
    response_model=List[MovimentacaoRead],
    summary="Lista movimentações da carteira do usuário autenticado",
)
def obter_movimentacoes(
    current_user: CurrentUser, # CORRIGIDO: Movido para antes dos argumentos com Query
    db: Session = Depends(get_db), # CORRIGIDO: Movido para antes dos argumentos com Query
    carteira_id: UUID = Query(..., description="ID da carteira"),
) -> List[MovimentacaoRead]:
    return listar_movimentacoes_por_carteira(
        db, carteira_id, usuario_id=current_user.id
    )