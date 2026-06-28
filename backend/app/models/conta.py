# FILE: backend/app/models/conta.py
from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import Moeda, StatusConta, TipoConta

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.instituicao import Instituicao
    from app.models.movimentacao import Movimentacao
    from app.models.aporte import Aporte
    from app.models.posicao import Posicao
    from app.models.provento import Provento
    from app.models.saldo_conta import SaldoConta


class Conta(TimestampMixin, Base):
    __tablename__ = "contas"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Isolamento por usuário — adicionado na Fase 3.6
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    instituicao_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("instituicoes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
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
    saldo_inicial: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )
    saldo_atual: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=Decimal("0.00"),
    )
    data_abertura: Mapped[date] = mapped_column(
        nullable=False,
    )
    status: Mapped[StatusConta] = mapped_column(
        Enum(StatusConta, name="status_conta_enum"),
        nullable=False,
        default=StatusConta.ATIVA,
    )

    # Relacionamentos
    usuario: Mapped["Usuario"] = relationship(back_populates="contas")
    instituicao: Mapped["Instituicao"] = relationship(back_populates="contas")
    movimentacoes: Mapped[List["Movimentacao"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )
    aportes: Mapped[List["Aporte"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )
    posicoes: Mapped[List["Posicao"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )
    proventos: Mapped[List["Provento"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )
    saldos_contas: Mapped[List["SaldoConta"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("saldo_atual >= 0", name="ck_contas_saldo_atual_nonneg"),
    )

    def __repr__(self) -> str:
        return f"<Conta(id='{self.id}', nome='{self.nome}', usuario_id='{self.usuario_id}')>"