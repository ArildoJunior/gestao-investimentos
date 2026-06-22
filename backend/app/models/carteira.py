# FILE: backend/app/models/carteira.py
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import ObjetivoCarteira, TipoCarteira

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.movimentacao import Movimentacao
    from app.models.aporte import Aporte
    from app.models.posicao import Posicao
    from app.models.provento import Provento

class Carteira(TimestampMixin, Base):
    __tablename__ = "carteiras"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    usuario_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    # Campos adicionados para corrigir os erros do pytest
    descricao: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    tipo: Mapped[TipoCarteira] = mapped_column(
        Enum(TipoCarteira, name="tipo_carteira_enum"),
        nullable=False,
        default=TipoCarteira.REAL,
    )
    objetivo: Mapped[ObjetivoCarteira] = mapped_column(
        Enum(ObjetivoCarteira, name="objetivo_carteira_enum"),
        nullable=False,
        default=ObjetivoCarteira.LIVRE,
    )
    saldo_inicial: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )
    saldo_atual: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relacionamentos
    usuario: Mapped["Usuario"] = relationship(
        back_populates="carteiras",
    )

    movimentacoes: Mapped[List["Movimentacao"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )

    aportes: Mapped[List["Aporte"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )

    posicoes: Mapped[List["Posicao"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )

    proventos: Mapped[List["Provento"]] = relationship(
        back_populates="carteira",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("saldo_atual >= 0", name="ck_carteiras_saldo_atual_nonneg"),
    )

    def __repr__(self):
        return f"<Carteira(id='{self.id}', nome='{self.nome}', usuario_id='{self.usuario_id}')>"