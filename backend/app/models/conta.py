from __future__ import annotations

import uuid

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TipoConta(str):
    CORRENTE = "CORRENTE"
    INVESTIMENTO = "INVESTIMENTO"
    POUPANCA = "POUPANCA"


class Moeda(str):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"


class StatusConta(str):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"


class Conta(TimestampMixin, Base):
    __tablename__ = "contas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    instituicao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("instituicoes.id", ondelete="RESTRICT"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    tipo: Mapped[str] = mapped_column(
        Enum(
            TipoConta.CORRENTE,
            TipoConta.INVESTIMENTO,
            TipoConta.POUPANCA,
            name="tipo_conta_enum",
        ),
        nullable=False,
    )

    moeda: Mapped[str] = mapped_column(
        Enum(Moeda.BRL, Moeda.USD, Moeda.EUR, name="moeda_enum"),
        nullable=False,
        default=Moeda.BRL,
    )

    saldo_atual: Mapped[float] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        Enum(StatusConta.ATIVA, StatusConta.INATIVA, name="status_conta_enum"),
        nullable=False,
        default=StatusConta.ATIVA,
    )

    instituicao: Mapped["Instituicao"] = relationship("Instituicao", backref="contas")