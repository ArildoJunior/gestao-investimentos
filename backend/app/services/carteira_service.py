from uuid import UUID
from sqlalchemy.orm import Session
from app.models.carteira import Carteira
from app.schemas.carteira import CarteiraCreate, CarteiraUpdate

def get_carteira(db: Session, carteira_id: UUID) -> Carteira | None:
    return db.query(Carteira).filter(Carteira.id == carteira_id).first()

def get_carteiras(db: Session, skip: int = 0, limit: int = 100) -> list[Carteira]:
    return db.query(Carteira).offset(skip).limit(limit).all()

def create_carteira(db: Session, carteira: CarteiraCreate) -> Carteira:
    db_carteira = Carteira(**carteira.model_dump())
    db.add(db_carteira)
    db.commit()
    db.refresh(db_carteira)
    return db_carteira

def update_carteira(db: Session, carteira_id: UUID, carteira: CarteiraUpdate) -> Carteira | None:
    db_carteira = db.query(Carteira).filter(Carteira.id == carteira_id).first()
    if db_carteira:
        for key, value in carteira.model_dump(exclude_unset=True).items():
            setattr(db_carteira, key, value)
        db.commit()
        db.refresh(db_carteira)
    return db_carteira

def delete_carteira(db: Session, carteira_id: UUID) -> Carteira | None:
    db_carteira = db.query(Carteira).filter(Carteira.id == carteira_id).first()
    if db_carteira:
        db.delete(db_carteira)
        db.commit()
    return db_carteira