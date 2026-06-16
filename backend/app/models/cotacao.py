from datetime import date
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class FonteCotacao(str, Enum):
    BRAPI = "BRAPI"
    YFINANCE = "YFINANCE"
    MANUAL = "MANUAL"


class Cotacao(TimestampMixin, Base):
    __tablename__ = "cotacoes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    ativo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ativos.id", ondelete="CASCADE"),
        nullable=False,
    )

    preco: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False)
    variacao_dia: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    volume: Mapped[float | None] = mapped_column(Numeric(20, 2), nullable=True)

    data_referencia: Mapped[date] = mapped_column(Date, nullable=False)

    fonte: Mapped[FonteCotacao] = mapped_column(
        SAEnum(FonteCotacao, name="fonte_cotacao_enum"),
        nullable=False,
    )

    ativo: Mapped["Ativo"] = relationship(
        "Ativo",
        backref="cotacoes",
    )