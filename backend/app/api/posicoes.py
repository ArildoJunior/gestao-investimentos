# FILE: backend/app/api/posicoes.py
# Este arquivo estava com um problema de importação de CurrentUser,
# e também com o Depends duplicado.

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser # CORREÇÃO: Importado CurrentUser de app.api.dependencies
from app.database import get_db
from app.schemas.posicao import PosicaoRead
from app.services.posicao_service import (
    get_posicao_by_carteira_and_ativo,
    get_posicoes_by_carteira,
    get_posicoes_by_carteira_and_conta,
)

router = APIRouter()

@router.get(
    "/carteira/{carteira_id}",
    response_model=list[PosicaoRead],
    summary="Lista todas as posições de uma carteira do usuário autenticado",
)
def read_posicoes_by_carteira(
    carteira_id: UUID,
    current_user: CurrentUser, # CORREÇÃO: Usar CurrentUser diretamente
    db: Session = Depends(get_db),
) -> list[PosicaoRead]:
    posicoes = get_posicoes_by_carteira(db, carteira_id, usuario_id=current_user.id)
    return [PosicaoRead.model_validate(p) for p in posicoes]

@router.get(
    "/carteira/{carteira_id}/conta/{conta_id}",
    response_model=list[PosicaoRead],
    summary="Lista posições de uma carteira filtradas por conta",
)
def read_posicoes_by_carteira_and_conta(
    carteira_id: UUID,
    conta_id: UUID,
    current_user: CurrentUser, # CORREÇÃO: Usar CurrentUser diretamente
    db: Session = Depends(get_db),
) -> list[PosicaoRead]:
    posicoes = get_posicoes_by_carteira_and_conta(
        db, carteira_id, conta_id, usuario_id=current_user.id
    )
    return [PosicaoRead.model_validate(p) for p in posicoes]

@router.get(
    "/carteira/{carteira_id}/ativo/{ativo_id}",
    response_model=PosicaoRead,
    summary="Busca posição específica de um ativo em uma carteira",
)
def get_posicao_por_carteira_e_ativo(
    carteira_id: UUID,
    ativo_id: UUID,
    current_user: CurrentUser, # CORREÇÃO: Usar CurrentUser diretamente
    db: Session = Depends(get_db),
) -> PosicaoRead:
    posicao = get_posicao_by_carteira_and_ativo(
        db, carteira_id, ativo_id, usuario_id=current_user.id
    )
    if not posicao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posição não encontrada para o ativo e carteira especificados.",
        )
    return PosicaoRead.model_validate(posicao)
