from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.models.base import Base


# Cria o engine usando a URL vinda do .env
engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
)

# Factory de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db() -> None:
    """Cria as tabelas se ainda não existirem (útil em dev)."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependência do FastAPI para obter uma sessão do banco."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()