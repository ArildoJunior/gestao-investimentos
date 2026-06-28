# FILE: backend/app/api/saldos_contas.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser # Importado CurrentUser
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
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> SaldoContaRead:
    try:
        return registrar_saldo_conta(db, payload, usuario_id=current_user.id)
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
    current_user: CurrentUser, # CORRIGIDO: Movido para antes dos argumentos com valor padrão
    db: Session = Depends(get_db),
    conta_id: UUID = Query(...), # CORRIGIDO: Movido para depois dos argumentos sem valor padrão
) -> List[SaldoContaRead]:
    return listar_saldos_conta(db, conta_id, usuario_id=current_user.id)

@router.get(
    "/{saldo_conta_id}",
    response_model=SaldoContaRead,
    summary="Busca lançamento de saldo por ID",
)
def get_saldo_conta(
    saldo_conta_id: UUID,
    current_user: CurrentUser, # CORRIGIDO: Removido = Depends(CurrentUser)
    db: Session = Depends(get_db),
) -> SaldoContaRead:
    item = get_saldo_conta_by_id(
        db, saldo_conta_id, usuario_id=current_user.id
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento de saldo não encontrado.",
        )
    return item
