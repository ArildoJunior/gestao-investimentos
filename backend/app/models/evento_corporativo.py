# FILE: backend/app/models/evento_corporativo.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4 # <-- Importado uuid4

from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    ForeignKey,
    Numeric,
    Text,
    # func, # <-- Removido func, pois não será usado para UUID
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import TipoEventoCorporativo

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.ativo import Ativo

class EventoCorporativo(TimestampMixin, Base):
    __tablename__ = "eventos_corporativos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4, # <-- Alterado para uuid4 do Python
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
        index=True,
    )

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    processado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    ativo: Mapped["Ativo"] = relationship(
        foreign_keys=[ativo_id],
        back_populates="eventos_corporativos_origem",
    )

    ativo_destino: Mapped["Ativo | None"] = relationship(
        foreign_keys=[ativo_destino_id],
        back_populates="eventos_corporativos_destino",
    )

    def __repr__(self) -> str:
        return (
            f"<EventoCorporativo(id={self.id}, ativo_id={self.ativo_id}, "
            f"tipo='{self.tipo.value}', data_evento={self.data_evento})>"
        )
