# FILE: backend/app/services/carteira_service.py
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.carteira import Carteira
from app.schemas.carteira import CarteiraCreate, CarteiraUpdate


def get_carteira(db: Session, carteira_id: UUID, usuario_id: UUID) -> Carteira | None:
    """Busca carteira garantindo que pertence ao usuário autenticado."""
    return (
        db.query(Carteira)
        .filter(Carteira.id == carteira_id, Carteira.usuario_id == usuario_id)
        .first()
    )


def get_carteiras(
    db: Session,
    usuario_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Carteira]:
    """Lista apenas as carteiras do usuário autenticado."""
    return (
        db.query(Carteira)
        .filter(Carteira.usuario_id == usuario_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_carteira(
    db: Session,
    carteira: CarteiraCreate,
    usuario_id: UUID,
) -> Carteira:
    """Cria carteira vinculada ao usuário autenticado."""
    data = carteira.model_dump()
    data["usuario_id"] = usuario_id  # sempre do token, nunca do payload
    db_carteira = Carteira(**data)
    db.add(db_carteira)
    db.commit()
    db.refresh(db_carteira)
    return db_carteira


def update_carteira(
    db: Session,
    carteira_id: UUID,
    carteira: CarteiraUpdate,
    usuario_id: UUID,
) -> Carteira | None:
    """Atualiza carteira somente se pertencer ao usuário autenticado."""
    db_carteira = get_carteira(db, carteira_id, usuario_id)
    if db_carteira is None:
        return None
    for key, value in carteira.model_dump(exclude_unset=True).items():
        setattr(db_carteira, key, value)
    db.commit()
    db.refresh(db_carteira)
    return db_carteira


def delete_carteira(
    db: Session,
    carteira_id: UUID,
    usuario_id: UUID,
) -> bool:
    """Deleta carteira somente se pertencer ao usuário autenticado."""
    db_carteira = get_carteira(db, carteira_id, usuario_id)
    if db_carteira is None:
        return False
    db.delete(db_carteira)
    db.commit()
    return True