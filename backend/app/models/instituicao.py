from __future__ import annotations

import uuid

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TipoInstituicao(str):
    CORRETORA = "CORRETORA"
    BANCO = "BANCO"
    OUTRO = "OUTRO"


class StatusInstituicao(str):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class Instituicao(TimestampMixin, Base):
    __tablename__ = "instituicoes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(
        Enum(
            TipoInstituicao.CORRETORA,
            TipoInstituicao.BANCO,
            TipoInstituicao.OUTRO,
            name="tipo_instituicao_enum",
        ),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Enum(
            StatusInstituicao.ATIVO,
            StatusInstituicao.INATIVO,
            name="status_instituicao_enum",
        ),
        nullable=False,
        default=StatusInstituicao.ATIVO,
    )