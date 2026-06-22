# FILE: backend/app/models/instituicao.py
from __future__ import annotations

from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4 # <-- Importado uuid4

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.sql import func # <-- Removido func, pois não será usado para UUID

from app.models.base import Base, TimestampMixin
from app.schemas.enums import StatusInstituicao, TipoInstituicao

if TYPE_CHECKING:
    from app.models.conta import Conta

class Instituicao(TimestampMixin, Base):
    __tablename__ = "instituicoes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4, # <-- Alterado para uuid4 do Python
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[TipoInstituicao] = mapped_column(
        Enum(TipoInstituicao, name="tipo_instituicao_enum"),
        nullable=False,
    )
    status: Mapped[StatusInstituicao] = mapped_column(
        Enum(StatusInstituicao, name="status_instituicao_enum"),
        nullable=False,
        default=StatusInstituicao.ATIVA,
    )

    # Relacionamentos
    contas: Mapped[List["Conta"]] = relationship(
        back_populates="instituicao",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Instituicao(id='{self.id}', nome='{self.nome}')>"
