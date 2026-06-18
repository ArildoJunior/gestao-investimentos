from __future__ import annotations

import enum
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.carteira import Carteira
    from app.models.conta import Conta
    from app.models.movimentacao import Movimentacao
    from app.models.provento import Provento


class TipoAporte(str, enum.Enum):
    EXTERNO = "EXTERNO"
    REINVESTIMENTO = "REINVESTIMENTO"


class OrigemAporte(str, enum.Enum):
    DIVIDENDO = "DIVIDENDO"
    JCP = "JCP"
    RENDIMENTO = "RENDIMENTO"
    JUROS_RF = "JUROS_RF"
    GANHO_CAPITAL = "GANHO_CAPITAL"
    OUTRO = "OUTRO"


class Aporte(TimestampMixin, Base):
    __tablename__ = "aportes"

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

    tipo: Mapped[TipoAporte] = mapped_column(
        Enum(TipoAporte, name="tipo_aporte_enum"),
        nullable=False,
        index=True,
    )

    origem: Mapped[OrigemAporte | None] = mapped_column(
        Enum(OrigemAporte, name="origem_aporte_enum"),
        nullable=True,
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    data_aporte: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    movimentacao_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("movimentacoes.id", ondelete="SET NULL"),
        nullable=True,
    )

    provento_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("proventos.id", ondelete="SET NULL"),
        nullable=True,
    )

    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)

    carteira: Mapped["Carteira"] = relationship(
        back_populates="aportes",
    )

    conta: Mapped["Conta | None"] = relationship(
        back_populates="aportes",
    )

    movimentacao: Mapped["Movimentacao | None"] = relationship(
        back_populates="aporte",
    )

    provento: Mapped["Provento | None"] = relationship(
        back_populates="aportes",
    )