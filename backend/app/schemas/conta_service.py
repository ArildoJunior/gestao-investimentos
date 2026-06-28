# FILE: backend/app/services/conta_service.py
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate, ContaUpdate


class ContaService:
    def __init__(self, db: Session):
        self.db = db

    def create_conta(self, conta: ContaCreate, usuario_id: UUID) -> Conta:
        """Cria conta vinculada ao usuário autenticado."""
        data = conta.model_dump()
        data["usuario_id"] = usuario_id  # sempre do token, nunca do payload
        db_conta = Conta(**data)
        self.db.add(db_conta)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def get_conta_by_id(self, conta_id: UUID, usuario_id: UUID) -> Optional[Conta]:
        """Busca conta garantindo que pertence ao usuário autenticado."""
        return (
            self.db.query(Conta)
            .filter(Conta.id == conta_id, Conta.usuario_id == usuario_id)
            .first()
        )

    def get_all_contas(
        self,
        usuario_id: UUID,
        skip: int = 0,
        limit: int = 100,
        instituicao_id: Optional[UUID] = None,
    ) -> List[Conta]:
        """Lista apenas as contas do usuário autenticado."""
        query = self.db.query(Conta).filter(Conta.usuario_id == usuario_id)
        if instituicao_id:
            query = query.filter(Conta.instituicao_id == instituicao_id)
        return query.offset(skip).limit(limit).all()

    def update_conta(
        self,
        conta_id: UUID,
        conta: ContaUpdate,
        usuario_id: UUID,
    ) -> Optional[Conta]:
        """Atualiza conta somente se pertencer ao usuário autenticado."""
        db_conta = self.get_conta_by_id(conta_id, usuario_id)
        if db_conta is None:
            return None
        for key, value in conta.model_dump(exclude_unset=True).items():
            setattr(db_conta, key, value)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def delete_conta(self, conta_id: UUID, usuario_id: UUID) -> bool:
        """Deleta conta somente se pertencer ao usuário autenticado."""
        db_conta = self.get_conta_by_id(conta_id, usuario_id)
        if db_conta is None:
            return False
        self.db.delete(db_conta)
        self.db.commit()
        return True