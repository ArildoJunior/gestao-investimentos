# FILE: backend/app/models/usuario.py
from __future__ import annotations

from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.carteira import Carteira
    from app.models.conta import Conta


class Usuario(TimestampMixin, Base):
    __tablename__ = "usuarios"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relacionamentos
    carteiras: Mapped[List["Carteira"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
    contas: Mapped[List["Conta"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Usuario(id='{self.id}', email='{self.email}')>"