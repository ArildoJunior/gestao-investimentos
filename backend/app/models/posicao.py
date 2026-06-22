# FILE: backend/app/models/posicao.py
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.carteira import Carteira
    from app.models.conta import Conta
    from app.models.ativo import Ativo

class Posicao(TimestampMixin, Base):
    __tablename__ = "posicoes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    carteira_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("carteiras.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    conta_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("contas.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    ativo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )

    preco_medio: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )

    # Adicionado o campo custo_total que estava faltando
    custo_total: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )

    # Relacionamentos
    carteira: Mapped["Carteira"] = relationship(
        back_populates="posicoes",
    )

    conta: Mapped["Conta"] = relationship(
        back_populates="posicoes",
    )

    ativo: Mapped["Ativo"] = relationship(
        back_populates="posicoes",
    )

    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="ck_posicoes_quantidade_nonneg"),
    )

    def __repr__(self):
        return (
            f"<Posicao(id={self.id}, carteira_id={self.carteira_id}, "
            f"ativo_id={self.ativo_id}, quantidade={self.quantidade}, "
            f"custo_total={self.custo_total})>"
        )