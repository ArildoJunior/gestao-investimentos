# FILE: backend/app/services/conta_service.py
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.models.carteira import Carteira
from app.schemas.conta import ContaCreate, ContaUpdate


class ContaService:
    def __init__(self, db: Session):
        self.db = db

    def _validar_carteira_usuario(
        self,
        carteira_id: UUID,
        usuario_id: UUID,
    ) -> Carteira:
        carteira = self.db.query(Carteira).filter(
            Carteira.id == carteira_id,
            Carteira.usuario_id == usuario_id,
        ).first()
        if carteira is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Carteira não encontrada ou não pertence ao usuário.",
            )
        return carteira

    def create_conta(
        self,
        conta: ContaCreate,
        usuario_id: UUID,
    ) -> Conta:
        # Valida se a instituição existe e se o usuário tem permissão para usá-la
        # (assumindo que instituições são globais ou que a validação ocorre em outro lugar)
        # Por enquanto, apenas cria a conta vinculada ao usuario_id
        db_conta = Conta(**conta.model_dump(), usuario_id=usuario_id)
        self.db.add(db_conta)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def get_all_contas(
        self,
        usuario_id: UUID,
        skip: int = 0,
        limit: int = 100,
        instituicao_id: UUID | None = None,
    ) -> list[Conta]:
        query = self.db.query(Conta).filter(Conta.usuario_id == usuario_id)
        if instituicao_id:
            query = query.filter(Conta.instituicao_id == instituicao_id)
        return query.offset(skip).limit(limit).all()

    def get_conta_by_id(
        self,
        conta_id: UUID,
        usuario_id: UUID,
    ) -> Conta | None:
        return self.db.query(Conta).filter(
            Conta.id == conta_id,
            Conta.usuario_id == usuario_id,
        ).first()

    def update_conta(
        self,
        conta_id: UUID,
        conta: ContaUpdate,
        usuario_id: UUID,
    ) -> Conta | None:
        db_conta = self.get_conta_by_id(conta_id, usuario_id)
        if db_conta is None:
            return None

        for key, value in conta.model_dump(exclude_unset=True).items():
            setattr(db_conta, key, value)

        self.db.add(db_conta)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def delete_conta(
        self,
        conta_id: UUID,
        usuario_id: UUID,
    ) -> bool:
        db_conta = self.get_conta_by_id(conta_id, usuario_id)
        if db_conta is None:
            return False

        self.db.delete(db_conta)
        self.db.commit()
        return True