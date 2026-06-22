# FILE: backend/app/services/posicao_service.py

from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.posicao import Posicao # Assumindo que você tem um modelo Posicao

def get_posicao_by_carteira_and_ativo(db: Session, carteira_id: UUID, ativo_id: UUID):
    return db.query(Posicao).filter(
        Posicao.carteira_id == carteira_id,
        Posicao.ativo_id == ativo_id
    ).first()

def get_posicoes_by_carteira(db: Session, carteira_id: UUID) -> List[Posicao]:
    return db.query(Posicao).filter(Posicao.carteira_id == carteira_id).all()

def get_posicoes_by_carteira_and_conta(db: Session, carteira_id: UUID, conta_id: UUID) -> List[Posicao]:
    return db.query(Posicao).filter(
        Posicao.carteira_id == carteira_id,
        Posicao.conta_id == conta_id # Assumindo que Posicao tem um campo conta_id
    ).all()