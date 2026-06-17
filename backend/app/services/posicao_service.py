from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.posicao import Posicao
from app.schemas.posicao import PosicaoRead


def listar_posicoes_por_carteira(
    db: Session,
    carteira_id: UUID,
    conta_id: UUID | None = None,
) -> list[PosicaoRead]:
    stmt = select(Posicao).where(Posicao.carteira_id == carteira_id)

    if conta_id is not None:
        stmt = stmt.where(Posicao.conta_id == conta_id)

    posicoes = db.scalars(stmt).all()
    return [PosicaoRead.model_validate(p) for p in posicoes]