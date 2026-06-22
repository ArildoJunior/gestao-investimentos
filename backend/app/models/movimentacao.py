from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import TipoMovimentacao, TipoOperacao

if TYPE_CHECKING:
    from app.models.aporte import Aporte
    from app.models.ativo import Ativo
    from app.models.carteira import Carteira
    from app.models.conta import Conta


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

    tipo_movimentacao: Mapped[TipoMovimentacao] = mapped_column(
        "tipo",
        Enum(TipoMovimentacao, name="tipo_movimentacao_enum"),
        nullable=False,
        index=True,
    )

    tipo_operacao: Mapped[TipoOperacao] = mapped_column(
        Enum(TipoOperacao, name="tipo_operacao_enum"),
        nullable=False,
        default=TipoOperacao.SWING,
    )

    data_operacao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    data_liquidacao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

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
        default=Decimal("0.00"),
    )

    emolumentos: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )

    iss: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )

    outras_taxas: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )

    valor_liquido: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    carteira: Mapped["Carteira"] = relationship(back_populates="movimentacoes")
    conta: Mapped["Conta"] = relationship(back_populates="movimentacoes")
    ativo: Mapped["Ativo"] = relationship(back_populates="movimentacoes")
    aporte: Mapped["Aporte | None"] = relationship(back_populates="movimentacao")

    def __repr__(self) -> str:
        return (
            f"<Movimentacao(id={self.id}, tipo_movimentacao={self.tipo_movimentacao.value}, "
            f"ativo_id={self.ativo_id}, quantidade={self.quantidade}, "
            f"preco_unitario={self.preco_unitario})>"
        )