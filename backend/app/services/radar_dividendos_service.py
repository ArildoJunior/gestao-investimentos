# FILE: backend/app/services/radar_dividendos_service.py
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.carteira import Carteira
from app.models.provento import Provento
from app.schemas.radar_dividendos import RadarDividendosItem, RadarDividendosFiltro


def _validar_carteira_usuario(
    db: Session,
    carteira_id: UUID,
    usuario_id: UUID,
) -> None:
    """Garante que a carteira pertence ao usuário autenticado."""
    carteira = (
        db.query(Carteira)
        .filter(
            Carteira.id == carteira_id,
            Carteira.usuario_id == usuario_id,
        )
        .first()
    )
    if not carteira:
        raise ValueError(
            "Carteira não encontrada ou não pertence ao usuário."
        )


def listar_radar_dividendos(
    db: Session,
    usuario_id: UUID,
    filtro: RadarDividendosFiltro,
) -> list[RadarDividendosItem]:
    """
    Retorna proventos com data_pagamento nos próximos N dias,
    isolados por usuário via carteira.
    """
    hoje = date.today()
    ate = hoje + timedelta(days=filtro.dias)

    # Valida a carteira se informada
    if filtro.carteira_id:
        _validar_carteira_usuario(db, filtro.carteira_id, usuario_id)

    # Busca carteiras do usuário para aplicar o filtro de isolamento
    carteiras_usuario = (
        db.query(Carteira.id)
        .filter(Carteira.usuario_id == usuario_id)
        .all()
    )
    ids_carteiras = [c.id for c in carteiras_usuario]

    if not ids_carteiras:
        return []

    query = (
        db.query(Provento)
        .options(joinedload(Provento.ativo))
        .filter(
            Provento.carteira_id.in_(ids_carteiras),
            Provento.data_pagamento >= hoje,
            Provento.data_pagamento <= ate,
        )
    )

    if filtro.carteira_id:
        query = query.filter(Provento.carteira_id == filtro.carteira_id)

    if filtro.ativo_id:
        query = query.filter(Provento.ativo_id == filtro.ativo_id)

    if filtro.apenas_nao_reinvestidos:
        query = query.filter(Provento.reinvestido == False)  # noqa: E712

    proventos = query.order_by(Provento.data_pagamento.asc()).all()

    resultado: list[RadarDividendosItem] = []
    for p in proventos:
        resultado.append(
            RadarDividendosItem(
                id=p.id,
                ativo_id=p.ativo_id,
                ticker=p.ativo.ticker if p.ativo else str(p.ativo_id),
                carteira_id=p.carteira_id,
                tipo=p.tipo,
                data_com=p.data_com,
                data_ex=p.data_ex,
                data_pagamento=p.data_pagamento,
                valor_bruto=p.valor_bruto,
                valor_liquido=p.valor_liquido,
                quantidade=p.quantidade_na_data or Decimal("0"),
                reinvestido=p.reinvestido,
            )
        )

    return resultado


def listar_historico_proventos(
    db: Session,
    usuario_id: UUID,
    carteira_id: UUID | None = None,
    ativo_id: UUID | None = None,
) -> list[RadarDividendosItem]:
    """
    Retorna todos os proventos passados do usuário (sem filtro de data futura).
    Útil para o histórico de renda passiva.
    """
    carteiras_usuario = (
        db.query(Carteira.id)
        .filter(Carteira.usuario_id == usuario_id)
        .all()
    )
    ids_carteiras = [c.id for c in carteiras_usuario]

    if not ids_carteiras:
        return []

    query = (
        db.query(Provento)
        .options(joinedload(Provento.ativo))
        .filter(Provento.carteira_id.in_(ids_carteiras))
    )

    if carteira_id:
        _validar_carteira_usuario(db, carteira_id, usuario_id)
        query = query.filter(Provento.carteira_id == carteira_id)

    if ativo_id:
        query = query.filter(Provento.ativo_id == ativo_id)

    proventos = query.order_by(Provento.data_pagamento.desc()).all()

    resultado: list[RadarDividendosItem] = []
    for p in proventos:
        resultado.append(
            RadarDividendosItem(
                id=p.id,
                ativo_id=p.ativo_id,
                ticker=p.ativo.ticker if p.ativo else str(p.ativo_id),
                carteira_id=p.carteira_id,
                tipo=p.tipo,
                data_com=p.data_com,
                data_ex=p.data_ex,
                data_pagamento=p.data_pagamento,
                valor_bruto=p.valor_bruto,
                valor_liquido=p.valor_liquido,
                quantidade=p.quantidade_na_data or Decimal("0"),
                reinvestido=p.reinvestido,
            )
        )

    return resultado