from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

from app.models.usuario import Usuario

class Carteira(TimestampMixin, Base):
    __tablename__ = "carteiras"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    # Ex.: "Real", "Simulada", "Teste", "Estratégia X"
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, default="Real")

    # Dono da carteira (no seu caso provavelmente 1 usuário só, mas já deixamos pronto)
    usuario_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
    )

    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Datas para filtros e histórico
    data_abertura: Mapped[datetime | None] = mapped_column(nullable=True)
    data_encerramento: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relacionamentos (serão usados depois)
    usuario: Mapped["Usuario"] = relationship("Usuario", backref="carteiras")