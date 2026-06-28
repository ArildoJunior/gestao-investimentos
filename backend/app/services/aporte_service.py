# FILE: backend/app/services/aporte_service.py
from uuid import UUID
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.aporte import Aporte
from app.schemas.aporte import AporteCreate, AporteRead

def _validar_pertence_ao_usuario(
    db: Session,
    carteira_id: UUID,
    conta_id: UUID,
    usuario_id: UUID,
) -> None:
    carteira = db.query(Carteira).filter(
        Carteira.id == carteira_id,
        Carteira.usuario_id == usuario_id,
    ).first()
    if not carteira:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Carteira não encontrada ou não pertence ao usuário.",
        )

    conta = db.query(Conta).filter(
        Conta.id == conta_id,
        Conta.usuario_id == usuario_id,
    ).first()
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta não encontrada ou não pertence ao usuário.",
        )

def registrar_aporte(
    db: Session,
    data: AporteCreate,
    usuario_id: UUID,
) -> AporteRead:
    _validar_pertence_ao_usuario(db, data.carteira_id, data.conta_id, usuario_id)

    aporte = Aporte(
        carteira_id=data.carteira_id,
        conta_id=data.conta_id,
        tipo=data.tipo,
        origem=data.origem,
        valor=data.valor,
        data_aporte=data.data_aporte,
        movimentacao_id=data.movimentacao_id,
        provento_id=data.provento_id,
        observacao=data.observacao,
    )

    db.add(aporte)
    db.commit()
    db.refresh(aporte)

    return AporteRead.model_validate(aporte)

def listar_aportes_por_carteira(
    db: Session,
    carteira_id: UUID,
    usuario_id: UUID,
    conta_id: Optional[UUID] = None,
) -> list[AporteRead]:
    # Valida que a carteira pertence ao usuário
    carteira = db.query(Carteira).filter(
        Carteira.id == carteira_id,
        Carteira.usuario_id == usuario_id,
    ).first()
    if not carteira:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Carteira não encontrada ou não pertence ao usuário.",
        )

    query = db.query(Aporte).filter(Aporte.carteira_id == carteira_id)

    if conta_id:
        query = query.filter(Aporte.conta_id == conta_id)

    aportes = query.order_by(Aporte.data_aporte.asc()).all()
    return [AporteRead.model_validate(a) for a in aportes]
