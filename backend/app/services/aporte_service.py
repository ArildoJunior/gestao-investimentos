from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session

from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.aporte import Aporte
from app.schemas.aporte import AporteCreate, AporteRead


def registrar_aporte(db: Session, data: AporteCreate) -> AporteRead:
    """
    Registra um aporte, validando carteira e conta, e persistindo o registro.

    Não faz, nesta fase, nenhum cálculo de rentabilidade ou evolução patrimonial.
    Esse papel será dos módulos core (rentabilidade, evolucao_patrimonial, etc.).
    """
    carteira = db.get(Carteira, data.carteira_id)
    if not carteira:
        raise ValueError("Carteira não encontrada.")

    conta = db.get(Conta, data.conta_id)
    if not conta:
        raise ValueError("Conta não encontrada.")

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
    conta_id: Optional[UUID] = None,
) -> list[AporteRead]:
    """
    Lista aportes de uma carteira, opcionalmente filtrando por conta.
    """
    query = db.query(Aporte).filter(Aporte.carteira_id == carteira_id)

    if conta_id:
        query = query.filter(Aporte.conta_id == conta_id)

    aportes = query.order_by(Aporte.data_aporte.asc()).all()

    return [AporteRead.model_validate(a) for a in aportes]