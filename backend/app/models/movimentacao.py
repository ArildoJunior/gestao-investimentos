from __future__ import annotations

import enum
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TipoMovimentacao(str, enum.Enum):
    COMPRA = "COMPRA"
    VENDA = "VENDA"


class TipoOperacao(str, enum.Enum):
    SWING = "SWING"
    DAY_TRADE = "DAY_TRADE"
    POSITION = "POSITION"


class Movimentacao(TimestampMixin, Base):
    __tablename__ = "movimentacoes"

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

    conta_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("contas.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    ativo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    tipo: Mapped[TipoMovimentacao] = mapped_column(
        Enum(TipoMovimentacao, name="tipo_movimentacao_enum"),
        nullable=False,
        index=True,
    )

    tipo_operacao: Mapped[TipoOperacao] = mapped_column(
        Enum(TipoOperacao, name="tipo_operacao_enum"),
        nullable=False,
        index=True,
    )

    data_operacao: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    data_liquidacao: Mapped[date | None] = mapped_column(Date, nullable=True)

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    valor_bruto: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    corretagem: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )

    emolumentos: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )

    iss: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )

    outras_taxas: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )

    valor_liquido: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    carteira: Mapped["Carteira"] = relationship(
        back_populates="movimentacoes",
    )
    conta: Mapped["Conta"] = relationship(
        back_populates="movimentacoes",
    )
    ativo: Mapped["Ativo"] = relationship(
        back_populates="movimentacoes",
    )