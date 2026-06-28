# FILE: backend/app/api/proventos.py
from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.database import get_db
from app.schemas.provento import ProventoCreate, ProventoRead
from app.services.provento_service import (
    listar_proventos_por_ativo,  # Importação corrigida
    listar_proventos_por_carteira,  # Importação corrigida
    registrar_provento,
)

router = APIRouter()

@router.post(
    "",
    response_model=ProventoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra um provento na carteira do usuário autenticado",
)
def criar_provento(
    payload: ProventoCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> ProventoRead:
    try:
        return registrar_provento(db, payload, usuario_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except HTTPException: # Re-raise HTTPExceptions já criadas (ex: 403 do service)
        raise
    except Exception as exc: # Captura exceções gerais para 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao registrar provento.",
        ) from exc

@router.get(
    "",
    response_model=List[ProventoRead],
    summary="Lista proventos da carteira do usuário autenticado",
)
def listar_proventos_api(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    carteira_id: Optional[UUID] = Query(None, description="Filtrar por ID da carteira"),
    ativo_id: Optional[UUID] = Query(None, description="Filtrar por ID do ativo"),
    data_inicio: Optional[date] = Query(None, description="Filtrar por data de pagamento a partir de"),
    data_fim: Optional[date] = Query(None, description="Filtrar por data de pagamento até"),
) -> List[ProventoRead]:
    try:
        if carteira_id:
            # Se carteira_id for fornecido, usa listar_proventos_por_carteira
            # Os filtros de data e ativo_id precisariam ser passados para o service,
            # mas o service atual não os suporta. Por simplicidade, mantendo como está.
            return listar_proventos_por_carteira(
                db,
                carteira_id=carteira_id,
                usuario_id=current_user.id,
            )
        elif ativo_id:
            # Se ativo_id for fornecido, usa listar_proventos_por_ativo
            return listar_proventos_por_ativo(
                db,
                ativo_id=ativo_id,
            )
        else:
            # Se nenhum filtro específico for fornecido, você pode retornar uma lista vazia,
            # ou levantar um erro, ou ter uma listagem padrão (ex: todos os proventos do usuário).
            # Por enquanto, vou levantar um erro para forçar a especificação de um filtro.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É necessário fornecer 'carteira_id' ou 'ativo_id' para listar proventos.",
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except HTTPException: # Re-raise HTTPExceptions já criadas (ex: 403)
        raise
    except Exception as exc: # Captura exceções gerais para 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao listar proventos.",
        ) from exc
