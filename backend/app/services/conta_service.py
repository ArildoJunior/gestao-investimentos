from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate, ContaUpdate


class ContaService:
    def __init__(self, db: Session):
        self.db = db

    def create_conta(self, conta: ContaCreate) -> Conta:
        db_conta = Conta(**conta.model_dump())
        self.db.add(db_conta)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def get_conta_by_id(self, conta_id: UUID) -> Optional[Conta]:
        return self.db.query(Conta).filter(Conta.id == conta_id).first()

    def get_all_contas(self, skip: int = 0, limit: int = 100, instituicao_id: Optional[UUID] = None) -> List[Conta]:
        query = self.db.query(Conta)
        if instituicao_id:
            query = query.filter(Conta.instituicao_id == instituicao_id)
        return query.offset(skip).limit(limit).all()

    def update_conta(self, conta_id: UUID, conta: ContaUpdate) -> Optional[Conta]:
        db_conta = self.get_conta_by_id(conta_id)
        if db_conta:
            for key, value in conta.model_dump(exclude_unset=True).items():
                setattr(db_conta, key, value)
            self.db.commit()
            self.db.refresh(db_conta)
            return db_conta
        return None

    def delete_conta(self, conta_id: UUID) -> bool:
        db_conta = self.get_conta_by_id(conta_id)
        if db_conta:
            self.db.delete(db_conta)
            self.db.commit()
            return True
        return False
