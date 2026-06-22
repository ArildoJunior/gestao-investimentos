# FILE: backend/app/services/ativo_service.py
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.schemas.ativo import AtivoCreate, AtivoUpdate


class AtivoService:
    def __init__(self, db: Session):
        self.db = db

    def create_ativo(self, ativo: AtivoCreate) -> Ativo:
        db_ativo = Ativo(**ativo.model_dump())
        self.db.add(db_ativo)
        self.db.commit()
        self.db.refresh(db_ativo)
        return db_ativo

    def get_ativo_by_id(self, ativo_id: UUID) -> Optional[Ativo]:
        # Usando db.get() para busca por chave primária
        return self.db.get(Ativo, ativo_id)

    def get_all_ativos(self, skip: int = 0, limit: int = 100) -> List[Ativo]:
        return self.db.query(Ativo).offset(skip).limit(limit).all()

    def update_ativo(self, ativo_id: UUID, ativo: AtivoUpdate) -> Optional[Ativo]:
        db_ativo = self.db.get(Ativo, ativo_id) # Usando db.get()
        if db_ativo:
            for key, value in ativo.model_dump(exclude_unset=True).items():
                setattr(db_ativo, key, value)
            self.db.commit()
            self.db.refresh(db_ativo)
            return db_ativo
        return None

    def delete_ativo(self, ativo_id: UUID) -> bool:
        db_ativo = self.db.get(Ativo, ativo_id) # Usando db.get()
        if db_ativo:
            self.db.delete(db_ativo)
            self.db.commit()
            return True
        return False
