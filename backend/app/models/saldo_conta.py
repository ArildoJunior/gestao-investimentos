from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TipoSaldoConta(str):
    DEPOSITO = "DEPOSITO"
    SAQUE = "SAQUE"
    TRANSFERENCIA = "TRANSFERENCIA"
    PIX = "PIX"
    TED = "TED"
    AJUSTE = "AJUSTE"


class SaldoConta(TimestampMixin, Base):
    __tablename__ = "saldos_contas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    conta_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contas.id", ondelete="CASCADE"),
        nullable=False,
    )

    tipo: Mapped[str] = mapped_column(
        Enum(
            TipoSaldoConta.DEPOSITO,
            TipoSaldoConta.SAQUE,
            TipoSaldoConta.TRANSFERENCIA,
            TipoSaldoConta.PIX,
            TipoSaldoConta.TED,
            TipoSaldoConta.AJUSTE,
            name="tipo_saldo_conta_enum",
        ),
        nullable=False,
    )

    valor: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False)

    data_operacao: Mapped[date] = mapped_column(Date, nullable=False)

    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    conta: Mapped["Conta"] = relationship("Conta", backref="saldos")