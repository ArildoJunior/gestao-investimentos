# FILE: backend/app/services/posicao_service.py
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.posicao import Posicao
from app.models.carteira import Carteira


def _validar_carteira_usuario(
    db: Session,
    carteira_id: UUID,
    usuario_id: UUID,
) -> None:
    carteira = db.query(Carteira).filter(
        Carteira.id == carteira_id,
        Carteira.usuario_id == usuario_id,
    ).first()
    if not carteira:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Carteira não encontrada ou não pertence ao usuário.",
        )


def get_posicao_by_carteira_and_ativo(
    db: Session,
    carteira_id: UUID,
    ativo_id: UUID,
    usuario_id: UUID,
) -> Posicao | None:
    _validar_carteira_usuario(db, carteira_id, usuario_id)
    return db.query(Posicao).filter(
        Posicao.carteira_id == carteira_id,
        Posicao.ativo_id == ativo_id,
    ).first()


def get_posicoes_by_carteira(
    db: Session,
    carteira_id: UUID,
    usuario_id: UUID,
) -> List[Posicao]:
    _validar_carteira_usuario(db, carteira_id, usuario_id)
    return db.query(Posicao).filter(
        Posicao.carteira_id == carteira_id,
    ).all()


def get_posicoes_by_carteira_and_conta(
    db: Session,
    carteira_id: UUID,
    conta_id: UUID,
    usuario_id: UUID,
) -> List[Posicao]:
    _validar_carteira_usuario(db, carteira_id, usuario_id)
    return db.query(Posicao).filter(
        Posicao.carteira_id == carteira_id,
        Posicao.conta_id == conta_id,
    ).all()