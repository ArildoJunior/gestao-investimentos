from __future__ import annotations

import uuid

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ClasseAtivo(str):
    ACAO = "ACAO"
    FII = "FII"
    ETF = "ETF"
    BDR = "BDR"
    REIT = "REIT"
    STOCK = "STOCK"
    CRIPTO = "CRIPTO"
    FUNDO = "FUNDO"
    OUTRO = "OUTRO"


class SegmentoFII(str):
    TIJOLO = "TIJOLO"
    PAPEL = "PAPEL"
    LOGISTICO = "LOGISTICO"
    SHOPPING = "SHOPPING"
    LAJES_CORPORATIVAS = "LAJES_CORPORATIVAS"
    HIBRIDO = "HIBRIDO"
    RECEBIVEL = "RECEBIVEL"
    FUNDO_DE_FUNDOS = "FUNDO_DE_FUNDOS"
    OUTRO = "OUTRO"


class Regiao(str):
    BRASIL = "BRASIL"
    AMERICA_NORTE = "AMERICA_NORTE"
    EUROPA = "EUROPA"
    ASIA = "ASIA"
    OUTRO = "OUTRO"


class StatusAtivo(str):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class Ativo(TimestampMixin, Base):
    __tablename__ = "ativos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ticker: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    classe: Mapped[str] = mapped_column(
        Enum(
            ClasseAtivo.ACAO,
            ClasseAtivo.FII,
            ClasseAtivo.ETF,
            ClasseAtivo.BDR,
            ClasseAtivo.REIT,
            ClasseAtivo.STOCK,
            ClasseAtivo.CRIPTO,
            ClasseAtivo.FUNDO,
            ClasseAtivo.OUTRO,
            name="classe_ativo_enum",
        ),
        nullable=False,
    )

    setor: Mapped[str | None] = mapped_column(String(255), nullable=True)

    segmento_fii: Mapped[str | None] = mapped_column(
        Enum(
            SegmentoFII.TIJOLO,
            SegmentoFII.PAPEL,
            SegmentoFII.LOGISTICO,
            SegmentoFII.SHOPPING,
            SegmentoFII.LAJES_CORPORATIVAS,
            SegmentoFII.HIBRIDO,
            SegmentoFII.RECEBIVEL,
            SegmentoFII.FUNDO_DE_FUNDOS,
            SegmentoFII.OUTRO,
            name="segmento_fii_enum",
        ),
        nullable=True,
    )

    pais: Mapped[str] = mapped_column(String(10), nullable=False, default="BR")

    regiao: Mapped[str] = mapped_column(
        Enum(
            Regiao.BRASIL,
            Regiao.AMERICA_NORTE,
            Regiao.EUROPA,
            Regiao.ASIA,
            Regiao.OUTRO,
            name="regiao_enum",
        ),
        nullable=False,
        default=Regiao.BRASIL,
    )

    moeda: Mapped[str] = mapped_column(
        Enum("BRL", "USD", "EUR", name="moeda_ativo_enum"),
        nullable=False,
        default="BRL",
    )

    status: Mapped[str] = mapped_column(
        Enum(StatusAtivo.ATIVO, StatusAtivo.INATIVO, name="status_ativo_enum"),
        nullable=False,
        default=StatusAtivo.ATIVO,
    )