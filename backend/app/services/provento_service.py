from decimal import Decimal
from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.provento import Provento
from app.models.aporte import Aporte
from app.schemas.provento import ProventoCreate, ProventoRead


def registrar_provento(
    db: Session,
    data: ProventoCreate,
    gerar_aporte_reinvestimento: bool = False,
    carteira_id: Optional[UUID] = None,
    conta_id: Optional[UUID] = None,
) -> ProventoRead:
    """
    Registra um provento.

    Se gerar_aporte_reinvestimento=True, cria também um Aporte REINVESTIMENTO
    vinculado a este provento, desde que carteira_id e conta_id sejam informados.
    """
    ativo = db.get(Ativo, data.ativo_id)
    if not ativo:
        raise ValueError("Ativo não encontrado.")

    valor_liquido = data.valor_bruto - data.ir_retido

    provento = Provento(
        ativo_id=data.ativo_id,
        tipo=data.tipo,
        valor_bruto=data.valor_bruto,
        ir_retido=data.ir_retido,
        valor_liquido=valor_liquido,
        data_com=data.data_com,
        data_ex=data.data_ex,
        data_pagamento=data.data_pagamento,
        quantidade_na_data=data.quantidade_na_data,
        reinvestido=data.reinvestido,
    )

    db.add(provento)
    db.flush()  # garante provento.id antes do commit

    # Opcional: gerar aporte de reinvestimento
    if gerar_aporte_reinvestimento:
        if not carteira_id or not conta_id:
            raise ValueError(
                "Para reinvestimento automático é necessário informar "
                "carteira_id e conta_id."
            )

        aporte = Aporte(
            carteira_id=carteira_id,
            conta_id=conta_id,
            tipo="REINVESTIMENTO",
            origem=data.tipo,  # DIVIDENDO, JCP, etc.
            valor=valor_liquido,
            data_aporte=data.data_pagamento,
            provento_id=provento.id,
            observacao="Reinvestimento automático de provento.",
        )
        db.add(aporte)

    db.commit()
    db.refresh(provento)

    return ProventoRead.model_validate(provento)


def listar_proventos_por_ativo(
    db: Session,
    ativo_id: UUID,
) -> list[ProventoRead]:
    """
    Lista todos os proventos de um ativo.
    """
    proventos = (
        db.query(Provento)
        .filter(Provento.ativo_id == ativo_id)
        .order_by(Provento.data_pagamento.asc())
        .all()
    )

    return [ProventoRead.model_validate(p) for p in proventos]