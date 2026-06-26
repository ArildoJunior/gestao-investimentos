# FILE: backend/app/api/proventos.py

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.provento import ProventoCreate, ProventoRead
from app.services.provento_service import (
    registrar_provento,
    listar_proventos_por_ativo,
    listar_proventos_por_carteira,  # vamos criar essa função
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
    carteira_id: Optional[UUID] = Query(None),
    ativo_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista proventos filtrados por carteira ou por ativo.
    Pelo menos um dos parâmetros deve ser informado.
    """
    if carteira_id:
        return listar_proventos_por_carteira(db, carteira_id)
    if ativo_id:
        return listar_proventos_por_ativo(db, ativo_id)
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Informe carteira_id ou ativo_id para filtrar os proventos.",
    )