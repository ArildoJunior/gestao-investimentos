from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import TipoProvento

if TYPE_CHECKING:
    from app.models.carteira import Carteira
    from app.models.conta import Conta
    from app.models.ativo import Ativo
    from app.models.aporte import Aporte


class Provento(TimestampMixin, Base):
    __tablename__ = "proventos"

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

    tipo: Mapped[TipoProvento] = mapped_column(
        Enum(TipoProvento, name="tipo_provento_enum"),
        nullable=False,
        index=True,
    )

    data_com: Mapped[date] = mapped_column(Date, nullable=False)
    data_pagamento: Mapped[date] = mapped_column(Date, nullable=False)

    valor_bruto: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    valor_liquido: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    reinvestido: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relacionamentos
    carteira: Mapped["Carteira"] = relationship(
        back_populates="proventos",
    )

    conta: Mapped["Conta | None"] = relationship(
        back_populates="proventos",
    )

    ativo: Mapped["Ativo"] = relationship(
        back_populates="proventos",
    )

    aportes: Mapped[List["Aporte"]] = relationship(
        back_populates="provento",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Provento(id={self.id}, tipo='{self.tipo.value}', "
            f"ativo_id={self.ativo_id}, valor_liquido={self.valor_liquido})>"
        )