from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.carteira import Carteira
    from app.models.conta import Conta
    from app.models.ativo import Ativo


class Posicao(Base):
    __tablename__ = "posicoes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    ativo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    carteira_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("carteiras.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    conta_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("contas.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    preco_medio: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    custo_total: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    carteira: Mapped["Carteira"] = relationship(
        back_populates="posicoes",
    )
    ativo: Mapped["Ativo"] = relationship(
        back_populates="posicoes",
    )
    conta: Mapped["Conta"] = relationship(
        back_populates="posicoes",
    )

    __table_args__ = (
        UniqueConstraint(
            "carteira_id",
            "ativo_id",
            "conta_id",
            name="uq_posicoes_carteira_ativo_conta",
        ),
        CheckConstraint("quantidade >= 0", name="ck_posicoes_quantidade_nonneg"),
        CheckConstraint("custo_total >= 0", name="ck_posicoes_custo_total_nonneg"),
    )