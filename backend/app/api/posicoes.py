from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.posicao import PosicaoRead
from app.services.posicao_service import (
    get_posicao_by_carteira_and_ativo,
    get_posicoes_by_carteira,
    get_posicoes_by_carteira_and_conta,
)

router = APIRouter()


@router.get("/carteira/{carteira_id}", response_model=list[PosicaoRead])
def read_posicoes_by_carteira(
    carteira_id: UUID,
    db: Session = Depends(get_db),
) -> list[PosicaoRead]:
    posicoes = get_posicoes_by_carteira(db, carteira_id)
    return [PosicaoRead.model_validate(posicao) for posicao in posicoes]


@router.get("/carteira/{carteira_id}/conta/{conta_id}", response_model=list[PosicaoRead])
def read_posicoes_by_carteira_and_conta(
    carteira_id: UUID,
    conta_id: UUID,
    db: Session = Depends(get_db),
) -> list[PosicaoRead]:
    posicoes = get_posicoes_by_carteira_and_conta(db, carteira_id, conta_id)
    return [PosicaoRead.model_validate(posicao) for posicao in posicoes]


@router.get("/carteira/{carteira_id}/ativo/{ativo_id}", response_model=PosicaoRead)
def get_posicao_por_carteira_e_ativo(
    carteira_id: UUID,
    ativo_id: UUID,
    db: Session = Depends(get_db),
) -> PosicaoRead:
    posicao = get_posicao_by_carteira_and_ativo(db, carteira_id, ativo_id)
    if not posicao:
        raise HTTPException(status_code=404, detail="Posição não encontrada para o ativo e carteira especificados.")
    return PosicaoRead.model_validate(posicao)