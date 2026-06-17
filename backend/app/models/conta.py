from __future__ import annotations

import enum
import uuid

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.instituicao import Instituicao
    from app.models.movimentacao import Movimentacao
    from app.models.aporte import Aporte
    from app.models.posicao import Posicao

class TipoConta(str, enum.Enum):
    CORRENTE = "CORRENTE"
    INVESTIMENTO = "INVESTIMENTO"
    POUPANCA = "POUPANCA"


class Moeda(str, enum.Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"


class StatusConta(str, enum.Enum):
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

    tipo: Mapped[TipoConta] = mapped_column(
        Enum(TipoConta, name="tipo_conta_enum"),
        nullable=False,
    )

    moeda: Mapped[Moeda] = mapped_column(
        Enum(Moeda, name="moeda_enum"),
        nullable=False,
        default=Moeda.BRL,
    )

    saldo_atual: Mapped[float] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=0,
    )

    status: Mapped[StatusConta] = mapped_column(
        Enum(StatusConta, name="status_conta_enum"),
        nullable=False,
        default=StatusConta.ATIVA,
    )

    instituicao: Mapped["Instituicao"] = relationship("Instituicao", backref="contas")

    movimentacoes: Mapped[list["Movimentacao"]] = relationship(
        back_populates="conta",
        cascade="all, delete-orphan",
    )

    aportes: Mapped[list["Aporte"]] = relationship(
        back_populates="conta",
        cascade="all, delete-orphan",
    )

    posicoes: Mapped[list["Posicao"]] = relationship(
        back_populates="conta",
        cascade="all, delete-orphan",
    )