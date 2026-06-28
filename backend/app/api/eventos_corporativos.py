# FILE: backend/app/api/eventos_corporativos.py
from __future__ import annotations

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.database import get_db
from app.schemas.evento_corporativo import (
    EventoCorporativoCreate,
    EventoCorporativoRead,
    # REMOVIDO: EventoCorporativoProcessar - não é usado e não existe no schema
)
from app.services.evento_corporativo_service import (
    listar_eventos_corporativos,
    processar_evento_corporativo,
    registrar_evento_corporativo,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "",
    response_model=EventoCorporativoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra um evento corporativo",
)
def criar_evento_corporativo(
    payload: EventoCorporativoCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> EventoCorporativoRead:
    try:
        # O usuario_id deve ser passado para o serviço para garantir o isolamento.
        # Assumindo que EventoCorporativoCreate não inclui usuario_id,
        # ele deve ser adicionado aqui ou no serviço.
        # Se o evento corporativo é um dado "global" de mercado, talvez não precise de usuario_id.
        # Se for um evento que afeta apenas o usuário, então o usuario_id é crucial.
        # Pelo contexto do "Dossiê Técnico", eventos corporativos são dados de mercado.
        # Portanto, o registro inicial pode não precisar de usuario_id.
        # Apenas o processamento do evento afeta as posições do usuário.
        return registrar_evento_corporativo(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.post(
    "/{evento_id}/processar",
    response_model=EventoCorporativoRead,
    summary="Processa um evento nas posições do usuário autenticado",
)
def processar_evento(
    evento_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> EventoCorporativoRead:
    try:
        return processar_evento_corporativo(
            db, evento_id, usuario_id=current_user.id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.get(
    "",
    response_model=List[EventoCorporativoRead],
    summary="Lista eventos corporativos (dados de mercado globais)",
)
def listar_eventos(
    current_user: CurrentUser, # CORRIGIDO: Movido para antes dos argumentos com valor padrão
    db: Session = Depends(get_db),
    ativo_id: UUID | None = Query(None),
) -> List[EventoCorporativoRead]:
    eventos = listar_eventos_corporativos(db, ativo_id=ativo_id)
    logger.info(
        "Consulta de eventos corporativos: ativo_id=%s, resultados=%d",
        ativo_id,
        len(eventos),
    )
    return [EventoCorporativoRead.model_validate(e) for e in eventos]
