from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.schemas.ativo import AtivoCreate, AtivoUpdate


def buscar_ativo_por_id(db: Session, ativo_id: UUID) -> Optional[Ativo]:
    """
    Busca um ativo pelo seu ID.
    """
    return db.query(Ativo).filter(Ativo.id == ativo_id).first()


def buscar_ativo_por_ticker(db: Session, ticker: str) -> Optional[Ativo]:
    """
    Busca um ativo pelo seu ticker.
    """
    return db.query(Ativo).filter(Ativo.ticker == ticker).first()


def listar_ativos(db: Session, skip: int = 0, limit: int = 100) -> List[Ativo]:
    """
    Lista todos os ativos.
    """
    return db.query(Ativo).offset(skip).limit(limit).all()


def criar_ativo(db: Session, ativo: AtivoCreate) -> Ativo:
    """
    Cria um novo ativo no banco de dados.
    """
    db_ativo = Ativo(**ativo.model_dump())
    db.add(db_ativo)
    db.commit()
    db.refresh(db_ativo)
    return db_ativo


def atualizar_ativo(
    db: Session, ativo_id: UUID, ativo_update: AtivoUpdate
) -> Optional[Ativo]:
    """
    Atualiza um ativo existente.
    """
    db_ativo = buscar_ativo_por_id(db, ativo_id)
    if db_ativo:
        for key, value in ativo_update.model_dump(exclude_unset=True).items():
            setattr(db_ativo, key, value)
        db.commit()
        db.refresh(db_ativo)
    return db_ativo


def deletar_ativo(db: Session, ativo_id: UUID) -> bool:
    """
    Deleta um ativo pelo seu ID.
    Retorna True se o ativo foi deletado, False caso contrário.
    """
    db_ativo = buscar_ativo_por_id(db, ativo_id)
    if db_ativo:
        db.delete(db_ativo)
        db.commit()
        return True
    return False
