# FILE: backend/app/models/saldo_conta.py
from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING # Adicionado TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.schemas.enums import TipoSaldoConta

# Adicionar esta importação para que Pylance possa resolver 'Conta'
# Mesmo que não seja usada diretamente no código, ajuda o Pylance
if TYPE_CHECKING:
    from app.models.conta import Conta

class SaldoConta(TimestampMixin, Base):
    __tablename__ = "saldos_contas"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4, # <-- Alterado para uuid.uuid4() do Python
    )

    conta_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("contas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tipo: Mapped[TipoSaldoConta] = mapped_column(
        Enum(TipoSaldoConta, name="tipo_saldo_conta_enum"),
        nullable=False,
    )

    valor: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)

    data_operacao: Mapped[date] = mapped_column(Date, nullable=False)

    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Referência à classe Conta como string literal
    conta: Mapped["Conta"] = relationship(
        back_populates="saldos_contas"
    )

    def __repr__(self) -> str:
        return f"<SaldoConta id={self.id}, conta_id={self.conta_id}, tipo={self.tipo.value}, valor={self.valor}>"
