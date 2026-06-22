from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.aporte import Aporte
from app.models.provento import Provento
from app.schemas.enums import TipoAporte, OrigemAporte, TipoProvento
from app.schemas.provento import ProventoCreate, ProventoRead


def registrar_provento(
    db: Session,
    data: ProventoCreate,
    gerar_aporte_reinvestimento: bool = False,
) -> ProventoRead:
    """
    Registra um provento.

    - Garante que o ativo exista.
    - Calcula valor_liquido (por enquanto = valor_bruto; IR detalhado virá na fase tributária).
    - Persiste o provento.
    - Opcionalmente, gera um Aporte de REINVESTIMENTO vinculado a este provento.
    """

    ativo = db.get(Ativo, data.ativo_id)
    if not ativo:
        raise ValueError("Ativo não encontrado.")

    if not data.carteira_id:
        raise ValueError("carteira_id é obrigatório para registrar provento.")

    valor_liquido: Decimal = data.valor_bruto  # sem ir_retido em banco nesta fase

    provento = Provento(
        carteira_id=data.carteira_id,
        conta_id=data.conta_id,
        ativo_id=data.ativo_id,
        tipo=data.tipo,
        data_com=data.data_com,
        data_pagamento=data.data_pagamento,
        valor_bruto=data.valor_bruto,
        valor_liquido=valor_liquido,
        quantidade=data.quantidade,
        reinvestido=data.reinvestido,
        observacoes=data.observacoes,
    )

    db.add(provento)
    db.flush()  # garante provento.id

    if gerar_aporte_reinvestimento and valor_liquido > 0:
        if not data.conta_id:
            raise ValueError(
                "Para reinvestimento automático é necessário informar conta_id."
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


def _mapear_origem_aporte(tipo_provento: TipoProvento) -> OrigemAporte:
    """
    Converte TipoProvento em OrigemAporte compatível com o Enum de aportes.
    """
    if tipo_provento == TipoProvento.DIVIDENDO:
        return OrigemAporte.DIVIDENDO
    if tipo_provento == TipoProvento.JCP:
        return OrigemAporte.JCP
    if tipo_provento == TipoProvento.RENDIMENTO:
        return OrigemAporte.RENDIMENTO
    if tipo_provento == TipoProvento.AMORTIZACAO:
        return OrigemAporte.AMORTIZACAO
    return OrigemAporte.OUTRO