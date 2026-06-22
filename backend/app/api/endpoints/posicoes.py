# FILE: backend/app/api/endpoints/posicoes.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.posicao import PosicaoRead # Assumindo que você tem um schema PosicaoRead
from app.services.posicao_service import get_posicao_by_carteira_and_ativo, get_posicoes_by_carteira, get_posicoes_by_carteira_and_conta # Assumindo um service

router = APIRouter()

@router.get("/carteira/{carteira_id}/ativo/{ativo_id}", response_model=PosicaoRead)
def read_posicao_by_carteira_and_ativo(
    carteira_id: UUID,
    ativo_id: UUID,
    db: Session = Depends(get_db)
):
    posicao = get_posicao_by_carteira_and_ativo(db, carteira_id, ativo_id)
    if not posicao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posição não encontrada")
    return posicao

@router.get("/carteira/{carteira_id}", response_model=List[PosicaoRead])
def read_posicoes_by_carteira(
    carteira_id: UUID,
    db: Session = Depends(get_db)
):
    posicoes = get_posicoes_by_carteira(db, carteira_id)
    return posicoes

@router.get("/carteira/{carteira_id}/conta/{conta_id}", response_model=List[PosicaoRead])
def read_posicoes_by_carteira_and_conta(
    carteira_id: UUID,
    conta_id: UUID,
    db: Session = Depends(get_db)
):
    posicoes = get_posicoes_by_carteira_and_conta(db, carteira_id, conta_id)
    return posicoes