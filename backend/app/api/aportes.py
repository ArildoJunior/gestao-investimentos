# FILE: backend/app/api/aportes.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser # Importa CurrentUser diretamente
from app.database import get_db
from app.schemas.aporte import AporteCreate, AporteRead
from app.services.aporte_service import listar_aportes_por_carteira, registrar_aporte

router = APIRouter()

@router.post(
    "",
    response_model=AporteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra um aporte na carteira do usuário autenticado",
)
def criar_aporte(
    payload: AporteCreate,
    current_user: CurrentUser, # Argumento sem valor padrão
    db: Session = Depends(get_db), # Argumento com valor padrão
) -> AporteRead:
    try:
        return registrar_aporte(db, payload, usuario_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.get(
    "",
    response_model=List[AporteRead],
    summary="Lista aportes da carteira do usuário autenticado",
)
def listar_aportes(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    carteira_id: UUID = Query(..., description="ID da carteira"),
    conta_id: UUID | None = Query(None, description="ID da conta (opcional)"),
) -> List[AporteRead]:
    # CORREÇÃO: Ajustada a ordem dos argumentos para corresponder à assinatura do service
    return listar_aportes_por_carteira(
        db, carteira_id, current_user.id, conta_id
    )
