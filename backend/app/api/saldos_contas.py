from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.saldo_conta import SaldoContaCreate, SaldoContaRead
from app.services.saldo_conta_service import (
    get_saldo_conta_by_id,
    listar_saldos_conta,
    registrar_saldo_conta,
)

router = APIRouter()


@router.post(
    "",
    response_model=SaldoContaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra movimentação de saldo da conta",
)
def create_saldo_conta(
    payload: SaldoContaCreate,
    db: Session = Depends(get_db),
) -> SaldoContaRead:
    try:
        return registrar_saldo_conta(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=List[SaldoContaRead],
    summary="Lista histórico de saldo por conta",
)
def get_saldos_conta(
    conta_id: UUID = Query(...),
    db: Session = Depends(get_db),
) -> List[SaldoContaRead]:
    return listar_saldos_conta(db, conta_id)


@router.get(
    "/{saldo_conta_id}",
    response_model=SaldoContaRead,
    summary="Busca lançamento de saldo por ID",
)
def get_saldo_conta(
    saldo_conta_id: UUID,
    db: Session = Depends(get_db),
) -> SaldoContaRead:
    item = get_saldo_conta_by_id(db, saldo_conta_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento de saldo não encontrado.",
        )
    return item