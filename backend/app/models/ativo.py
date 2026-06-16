from __future__ import annotations

import enum
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ClasseAtivo(str, enum.Enum):
    ACAO = "ACAO"
    FII = "FII"
    ETF = "ETF"
    BDR = "BDR"
    REIT = "REIT"
    STOCK = "STOCK"
    CRIPTO = "CRIPTO"
    FUNDO = "FUNDO"
    OUTRO = "OUTRO"


class SegmentoFII(str, enum.Enum):
    TIJOLO = "TIJOLO"
    PAPEL = "PAPEL"
    LOGISTICO = "LOGISTICO"
    SHOPPING = "SHOPPING"
    LAJES_CORPORATIVAS = "LAJES_CORPORATIVAS"
    HIBRIDO = "HIBRIDO"
    RECEBIVEL = "RECEBIVEL"
    FUNDO_DE_FUNDOS = "FUNDO_DE_FUNDOS"
    OUTRO = "OUTRO"


class Regiao(str, enum.Enum):
    BRASIL = "BRASIL"
    AMERICA_NORTE = "AMERICA_NORTE"
    EUROPA = "EUROPA"
    ASIA = "ASIA"
    OUTRO = "OUTRO"


class StatusAtivo(str, enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class Ativo(TimestampMixin, Base):
    __tablename__ = "ativos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    ticker: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    classe: Mapped[ClasseAtivo] = mapped_column(
        Enum(ClasseAtivo, name="classe_ativo_enum"),
        nullable=False,
    )

    setor: Mapped[str | None] = mapped_column(String(255), nullable=True)

    segmento_fii: Mapped[SegmentoFII | None] = mapped_column(
        Enum(SegmentoFII, name="segmento_fii_enum"),
        nullable=True,
    )

    pais: Mapped[str] = mapped_column(String(10), nullable=False, default="BR")

    regiao: Mapped[Regiao] = mapped_column(
        Enum(Regiao, name="regiao_enum"),
        nullable=False,
        default=Regiao.BRASIL,
    )

    moeda: Mapped[str] = mapped_column(
        Enum("BRL", "USD", "EUR", name="moeda_ativo_enum"),
        nullable=False,
        default="BRL",
    )

    status: Mapped[StatusAtivo] = mapped_column(
        Enum(StatusAtivo, name="status_ativo_enum"),
        nullable=False,
        default=StatusAtivo.ATIVO,
    )

    # Relacionamentos (tipos em string; não precisa importar as classes aqui)
    movimentacoes: Mapped[list["Movimentacao"]] = relationship(
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    posicoes: Mapped[list["Posicao"]] = relationship(
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    proventos: Mapped[list["Provento"]] = relationship(
        back_populates="ativo",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Ativo ticker={self.ticker} classe={self.classe}>"