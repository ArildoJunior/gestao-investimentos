from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate, ContaUpdate


def criar_conta(db: Session, conta: ContaCreate) -> Conta:
    """
    Cria uma nova conta no banco de dados.
    """
    db_conta = Conta(**conta.model_dump())
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta


def buscar_conta_por_id(db: Session, conta_id: UUID) -> Optional[Conta]:
    """
    Busca uma conta pelo seu ID.
    """
    return db.query(Conta).filter(Conta.id == conta_id).first()


def listar_contas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    instituicao_id: Optional[UUID] = None,
) -> List[Conta]:
    """
    Lista todas as contas, opcionalmente filtrando por instituição.
    """
    query = db.query(Conta)
    if instituicao_id:
        query = query.filter(Conta.instituicao_id == instituicao_id)
    return query.offset(skip).limit(limit).all()


def atualizar_conta(
    db: Session, conta_id: UUID, conta_update: ContaUpdate
) -> Optional[Conta]:
    """
    Atualiza uma conta existente.
    """
    db_conta = buscar_conta_por_id(db, conta_id)
    if db_conta:
        for key, value in conta_update.model_dump(exclude_unset=True).items():
            setattr(db_conta, key, value)
        db.commit()
        db.refresh(db_conta)
    return db_conta


def deletar_conta(db: Session, conta_id: UUID) -> bool:
    """
    Deleta uma conta pelo seu ID.
    Retorna True se a conta foi deletada, False caso contrário.
    """
    db_conta = buscar_conta_por_id(db, conta_id)
    if db_conta:
        db.delete(db_conta)
        db.commit()
        return True
    return False