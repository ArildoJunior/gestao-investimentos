from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.provento import ProventoCreate, ProventoRead
from app.services.provento_service import (
    registrar_provento,
    listar_proventos_por_ativo,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ProventoRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_provento(
    payload: ProventoCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um registro de provento (dividendos, JCP, rendimentos, amortização).

    Nesta fase, o reinvestimento automático é opcional e controlado na camada de serviço.
    """
    try:
        return registrar_provento(db, payload, gerar_aporte_reinvestimento=False)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[ProventoRead],
)
def listar_proventos(
    ativo_id: UUID = Query(...),
    db: Session = Depends(get_db),
):
    """
    Lista proventos por ativo.
    """
    return listar_proventos_por_ativo(db, ativo_id)