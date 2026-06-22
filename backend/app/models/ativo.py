# FILE: backend/app/models/ativo.py
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4 # <-- Importado uuid4

from sqlalchemy import Boolean, DateTime, Enum, String, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.sql import func # <-- Removido func, pois não será usado para UUID

from app.models.base import Base, TimestampMixin
from app.schemas.enums import TipoAtivo, SegmentoFII, RegiaoAtivo, StatusAtivo, Moeda

if TYPE_CHECKING:
    from app.models.carteira import Carteira
    from app.models.movimentacao import Movimentacao
    from app.models.posicao import Posicao
    from app.models.provento import Provento
    from app.models.evento_corporativo import EventoCorporativo
    from app.models.cotacao import Cotacao # <-- Adicionado import para Cotacao

class Ativo(TimestampMixin, Base):
    __tablename__ = "ativos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4, # <-- Alterado para uuid4 do Python
    )
    ticker: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    classe: Mapped[TipoAtivo] = mapped_column(
        Enum(TipoAtivo, name="classe_ativo_enum"),
        nullable=False,
    )
    setor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    segmento_fii: Mapped[SegmentoFII | None] = mapped_column(
        Enum(SegmentoFII, name="segmento_fii_enum"),
        nullable=True,
    )
    pais: Mapped[str] = mapped_column(String(2), nullable=False, default="BR")
    regiao: Mapped[RegiaoAtivo] = mapped_column(
        Enum(RegiaoAtivo, name="regiao_enum"),
        nullable=False,
        default=RegiaoAtivo.BRASIL,
    )
    moeda: Mapped[Moeda] = mapped_column(
        Enum(Moeda, name="moeda_ativo_enum"),
        nullable=False,
        default=Moeda.BRL,
    )
    status: Mapped[StatusAtivo] = mapped_column(
        Enum(StatusAtivo, name="status_ativo_enum"),
        nullable=False,
        default=StatusAtivo.ATIVO,
    )

    # Relacionamentos
    movimentacoes: Mapped[List["Movimentacao"]] = relationship(
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    posicoes: Mapped[List["Posicao"]] = relationship(
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    proventos: Mapped[List["Provento"]] = relationship(
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    # Relacionamentos para Eventos Corporativos, agora separados e explícitos
    eventos_corporativos_origem: Mapped[List["EventoCorporativo"]] = relationship(
        "EventoCorporativo",
        foreign_keys="[EventoCorporativo.ativo_id]",
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    eventos_corporativos_destino: Mapped[List["EventoCorporativo"]] = relationship(
        "EventoCorporativo",
        foreign_keys="[EventoCorporativo.ativo_destino_id]",
        back_populates="ativo_destino",
        cascade="all, delete-orphan",
    )

    cotacoes: Mapped[List["Cotacao"]] = relationship( # <-- Adicionado relacionamento cotacoes
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Ativo ticker={self.ticker} classe={self.classe.value}>"
