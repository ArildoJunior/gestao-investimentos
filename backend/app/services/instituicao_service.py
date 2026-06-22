from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.instituicao import Instituicao
from app.schemas.instituicao import InstituicaoCreate, InstituicaoUpdate


class InstituicaoService:
    def __init__(self, db: Session):
        self.db = db

    def create_instituicao(self, instituicao: InstituicaoCreate) -> Instituicao:
        db_instituicao = Instituicao(**instituicao.model_dump())
        self.db.add(db_instituicao)
        self.db.commit()
        self.db.refresh(db_instituicao)
        return db_instituicao

    def get_all_instituicoes(self, skip: int = 0, limit: int = 100) -> List[Instituicao]:
        return self.db.query(Instituicao).offset(skip).limit(limit).all()

    def get_instituicao_by_id(self, instituicao_id: UUID) -> Optional[Instituicao]:
        return self.db.query(Instituicao).filter(Instituicao.id == instituicao_id).first()

    def update_instituicao(self, instituicao_id: UUID, instituicao_update: InstituicaoUpdate) -> Optional[Instituicao]:
        db_instituicao = self.get_instituicao_by_id(instituicao_id)
        if db_instituicao:
            for key, value in instituicao_update.model_dump(exclude_unset=True).items():
                setattr(db_instituicao, key, value)
            self.db.commit()
            self.db.refresh(db_instituicao)
        return db_instituicao

    def delete_instituicao(self, instituicao_id: UUID) -> bool:
        db_instituicao = self.get_instituicao_by_id(instituicao_id)
        if db_instituicao:
            self.db.delete(db_instituicao)
            self.db.commit()
            return True
        return False
