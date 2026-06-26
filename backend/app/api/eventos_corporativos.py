# FILE: backend/app/api/eventos_corporativos.py

from typing import List, Optional
from uuid import UUID
import logging # Importar o módulo logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.evento_corporativo import (
    EventoCorporativoCreate,
    EventoCorporativoRead,
)
from app.services.evento_corporativo_service import (
    registrar_evento_corporativo,
    processar_evento_corporativo,
)
from app.models.evento_corporativo import EventoCorporativo

router = APIRouter()

# Configurar o logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Definir o nível de log

@router.post(
    "/",
    response_model=EventoCorporativoRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_evento_corporativo(
    payload: EventoCorporativoCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um registro de evento corporativo (sem processar posições ainda).
    """
    try:
        return registrar_evento_corporativo(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post(
    "/{evento_id}/processar",
    response_model=EventoCorporativoRead,
)
def processar_evento(
    evento_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Processa um evento corporativo, aplicando seus efeitos às posições
    do ativo de origem.
    """
    try:
        return processar_evento_corporativo(db, evento_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

# Rota GET para listar eventos (agora com ativo_id opcional)
@router.get(
    "/",
    response_model=List[EventoCorporativoRead],
)
def listar_eventos_corporativos(
    ativo_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista eventos corporativos. Pode ser filtrado por ativo_id.
    """
    query = db.query(EventoCorporativo)
    if ativo_id:
        query = query.filter(EventoCorporativo.ativo_id == ativo_id)

    eventos = query.order_by(EventoCorporativo.data_evento.asc()).all()

    # --- ADICIONAR ESTE LOG ---
    logger.info(f"Consulta de eventos corporativos: ativo_id={ativo_id}, resultados={len(eventos)}")
    for evento in eventos:
        logger.info(f"  - Evento ID: {evento.id}, Tipo: {evento.tipo}, Data: {evento.data_evento}")
    # -------------------------

    return [EventoCorporativoRead.model_validate(e) for e in eventos]
