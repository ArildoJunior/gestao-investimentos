# FILE: backend/app/models/base.py
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4 # <-- Importado uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.
    """

    __abstract__ = True
    # generate automatically table name based on class name
    # __tablename__ = ColumnOperators.info_for_mapper(lambda cls: cls.__name__.lower())

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4, # <-- Alterado para uuid4 do Python
    )

    # Adiciona um método repr genérico para facilitar a depuração
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


class TimestampMixin:
    """Mixin para adicionar campos de timestamp created_at e updated_at."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
