# FILE: backend/app/models/cotacao.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4 # <-- Importado uuid4

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.ativo import Ativo

class Cotacao(TimestampMixin, Base):
    __tablename__ = "cotacoes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4, # <-- Alterado para uuid4 do Python
    )
    ativo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    data: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)

    ativo: Mapped["Ativo"] = relationship(
        back_populates="cotacoes"
    )

    def __repr__(self) -> str:
        return f"<Cotacao id={self.id}, ativo_id={self.ativo_id}, data={self.data}, valor={self.valor}>"
