from __future__ import annotations

import enum
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Date, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movimentacao import Movimentacao
    from app.models.posicao import Posicao
    from app.models.provento import Provento
    from app.models.ativo import Ativo
    from app.models.aporte import Aporte


class TipoProvento(str, enum.Enum):
    DIVIDENDO = "DIVIDENDO"
    JCP = "JCP"
    RENDIMENTO = "RENDIMENTO"
    AMORTIZACAO = "AMORTIZACAO"


class Provento(TimestampMixin, Base):
    __tablename__ = "proventos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    ativo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tipo: Mapped[TipoProvento] = mapped_column(
        Enum(TipoProvento, name="tipo_provento_enum"),
        nullable=False,
        index=True,
    )

    valor_bruto: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    ir_retido: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0"),
    )

    valor_liquido: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    data_com: Mapped[date] = mapped_column(Date, nullable=False)
    data_ex: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_pagamento: Mapped[date | None] = mapped_column(Date, nullable=True)

    quantidade_na_data: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 8),
        nullable=True,
    )

    reinvestido: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    # Relacionamentos
    ativo: Mapped["Ativo"] = relationship(back_populates="proventos")
    aportes_relacionados: Mapped[list["Aporte"]] = relationship(
        back_populates="provento",
        cascade="all, delete-orphan",
    )