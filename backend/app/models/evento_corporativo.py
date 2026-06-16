from __future__ import annotations

import enum
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TipoEventoCorporativo(str, enum.Enum):
    SPLIT = "SPLIT"
    GRUPAMENTO = "GRUPAMENTO"
    BONIFICACAO = "BONIFICACAO"
    SUBSCRICAO = "SUBSCRICAO"
    AMORTIZACAO = "AMORTIZACAO"
    INCORPORACAO = "INCORPORACAO"
    FUSAO = "FUSAO"
    CISAO = "CISAO"


class EventoCorporativo(TimestampMixin, Base):
    __tablename__ = "eventos_corporativos"

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

    tipo: Mapped[TipoEventoCorporativo] = mapped_column(
        Enum(TipoEventoCorporativo, name="tipo_evento_corporativo_enum"),
        nullable=False,
        index=True,
    )

    data_evento: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    fator: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    valor: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 8),
        nullable=True,
    )

    ativo_destino_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="SET NULL"),
        nullable=True,
    )

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    processado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    ativo: Mapped["Ativo"] = relationship(
        "Ativo",
        foreign_keys=[ativo_id],
        backref="eventos_corporativos_origem",
    )

    ativo_destino: Mapped["Ativo"] = relationship(
        "Ativo",
        foreign_keys=[ativo_destino_id],
        backref="eventos_corporativos_destino",
    )