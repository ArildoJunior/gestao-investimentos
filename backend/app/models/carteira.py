from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Carteira(TimestampMixin, Base):
    __tablename__ = "carteiras"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    # Ex.: "Real", "Simulada", "Teste", "Estratégia X"
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, default="Real")

    # Por enquanto não vamos amarrar a usuário; se quiser isso mais tarde, adicionamos usuario_id
    # usuario_id: Mapped[UUID] = mapped_column(
    #     PG_UUID(as_uuid=True),
    #     ForeignKey("usuarios.id", ondelete="CASCADE"),
    #     nullable=False,
    # )

    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Datas para filtros e histórico
    data_abertura: Mapped[datetime | None] = mapped_column(nullable=True)
    data_encerramento: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relacionamentos (serão usados depois)
    movimentacoes: Mapped[list["Movimentacao"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )

    aportes: Mapped[list["Aporte"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )

    posicoes: Mapped[list["Posicao"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )