# FILE: backend/app/models/provento.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import TipoProvento

if TYPE_CHECKING:
    from app.models.ativo import Ativo
    from app.models.carteira import Carteira
    from app.models.conta import Conta # Importação de Conta
    from app.models.aporte import Aporte


class Provento(TimestampMixin, Base):
    __tablename__ = "proventos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ativo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("ativos.id"))
    carteira_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("carteiras.id")
    )
    # ADICIONADO: ForeignKey para contas.id
    conta_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("contas.id"))

    tipo: Mapped[TipoProvento] = mapped_column(Enum(TipoProvento, name="tipoprovento"))
    valor_bruto: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    ir_retido: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0.00"))
    valor_liquido: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    data_com: Mapped[date] = mapped_column(Date)
    data_ex: Mapped[Optional[date]] = mapped_column(Date, nullable=True) # Pode ser nulo
    data_pagamento: Mapped[date] = mapped_column(Date)
    quantidade_na_data: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0.00")
    )
    reinvestido: Mapped[bool] = mapped_column(Boolean, default=False)
    observacoes: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # Pode ser nulo

    # Relacionamentos
    ativo: Mapped["Ativo"] = relationship(back_populates="proventos")
    carteira: Mapped["Carteira"] = relationship(back_populates="proventos")
    conta: Mapped["Conta"] = relationship(back_populates="proventos") # Relação com Conta
    aportes: Mapped[List["Aporte"]] = relationship(back_populates="provento")

    def __repr__(self) -> str:
        return (
            f"<Provento(id={self.id}, tipo='{self.tipo.value}', "
            f"ativo_id={self.ativo_id}, valor_liquido={self.valor_liquido})>"
        )
