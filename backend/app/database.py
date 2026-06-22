# FILE: backend/app/database.py
from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker # Removido declarative_base

from app.config import settings
from app.models.base import Base # <-- Importa a Base de app.models.base

engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
)

# SessionLocal será a classe que criará novas sessões de banco de dados
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependência para obter uma sessão de banco de dados.
    Usada pelo FastAPI para injetar a sessão nos endpoints.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Para testes, a criação das tabelas será feita diretamente no conftest.py.