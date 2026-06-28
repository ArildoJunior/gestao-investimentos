# FILE: backend/app/services/provento_service.py
from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.aporte import Aporte
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.provento import Provento
from app.schemas.aporte import AporteCreate
from app.schemas.enums import OrigemAporte, TipoAporte, TipoProvento
from app.schemas.provento import ProventoCreate, ProventoRead

def _validar_pertence_ao_usuario(
    db: Session,
    carteira_id: UUID,
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

def registrar_provento(
    db: Session,
    data: ProventoCreate,
    usuario_id: UUID,
    gerar_aporte_reinvestimento: bool = False,
) -> ProventoRead:
    try:
        _validar_pertence_ao_usuario(db, data.carteira_id, usuario_id)

        ir_retido = data.ir_retido
        valor_liquido = data.valor_bruto - ir_retido

        provento = Provento(
            ativo_id=data.ativo_id,
            carteira_id=data.carteira_id,
            conta_id=data.conta_id, # <--- ADICIONADO: Passando o conta_id do payload
            tipo=data.tipo,
            valor_bruto=data.valor_bruto,
            ir_retido=ir_retido,
            valor_liquido=valor_liquido,
            data_com=data.data_com,
            data_ex=data.data_ex,
            data_pagamento=data.data_pagamento,
            quantidade_na_data=data.quantidade_na_data,
            reinvestido=gerar_aporte_reinvestimento,
            observacoes=data.observacoes,
        )

        db.add(provento)
        db.flush()

        if gerar_aporte_reinvestimento and valor_liquido > 0:
            if not data.conta_id:
                raise ValueError(
                    "Para reinvestimento automático é necessário informar conta_id."
                )

            conta = db.query(Conta).filter(
                Conta.id == data.conta_id,
                Conta.usuario_id == usuario_id,
            ).first()
            if not conta:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Conta não encontrada ou não pertence ao usuário.",
                )

            aporte = Aporte(
                carteira_id=data.carteira_id,
                conta_id=data.conta_id,
                tipo=TipoAporte.REINVESTIMENTO,
                origem=_mapear_origem_aporte(data.tipo),
                valor=valor_liquido,
                data_aporte=data.data_pagamento,
                provento_id=provento.id,
                observacao="Reinvestimento automático de provento.",
            )
            db.add(aporte)

        db.commit()
        db.refresh(provento)

        return ProventoRead.model_validate(provento)
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de integridade no banco de dados: {exc.orig}",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise

def listar_proventos_por_ativo(
    db: Session,
    ativo_id: UUID,
) -> list[ProventoRead]:
    """
    Proventos por ativo são públicos (não dependem de usuário) —
    são dados do ativo, não da carteira.
    """
    proventos = (
        db.query(Provento)
        .filter(Provento.ativo_id == ativo_id)
        .order_by(Provento.data_pagamento.asc())
        .all()
    )
    return [ProventoRead.model_validate(p) for p in proventos]

def listar_proventos_por_carteira(
    db: Session,
    carteira_id: UUID,
    usuario_id: UUID,
) -> list[ProventoRead]:
    _validar_pertence_ao_usuario(db, carteira_id, usuario_id)

    proventos = (
        db.query(Provento)
        .filter(Provento.carteira_id == carteira_id)
        .order_by(Provento.data_pagamento.desc())
        .all()
    )
    return [ProventoRead.model_validate(p) for p in proventos]

def _mapear_origem_aporte(tipo_provento: TipoProvento) -> OrigemAporte:
    if tipo_provento == TipoProvento.DIVIDENDO:
        return OrigemAporte.DIVIDENDO
    if tipo_provento == TipoProvento.JCP:
        return OrigemAporte.JCP
    if tipo_provento == TipoProvento.RENDIMENTO:
        return OrigemAporte.RENDIMENTO
    if tipo_provento == TipoProvento.AMORTIZACAO:
        return OrigemAporte.AMORTIZACAO
    return OrigemAporte.OUTRO
