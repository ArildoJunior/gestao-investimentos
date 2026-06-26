from __future__ import annotations

from typing import List # Importar List para tipagem
from uuid import UUID # Importar UUID para tipagem

from fastapi import APIRouter, Depends, HTTPException, status, Query # Importar Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoRead
from app.services.movimentacao_service import registrar_movimentacao, listar_movimentacoes_por_carteira # Importar novo serviço

router = APIRouter()

@router.post(
    "",
    response_model=MovimentacaoRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_movimentacao(
    payload: MovimentacaoCreate,
    db: Session = Depends(get_db),
) -> MovimentacaoRead:
    try:
        return registrar_movimentacao(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

# NOVA ROTA GET PARA LISTAR MOVIMENTAÇÕES
@router.get(
    "",
    response_model=List[MovimentacaoRead], # Retorna uma lista de MovimentacaoRead
    status_code=status.HTTP_200_OK,
)
def obter_movimentacoes(
    carteira_id: UUID = Query(..., description="ID da carteira para filtrar as movimentações"), # Parâmetro de query
    db: Session = Depends(get_db),
) -> List[MovimentacaoRead]:
    """
    Obtém uma lista de movimentações filtradas por carteira.
    """
    try:
        movimentacoes = listar_movimentacoes_por_carteira(db, carteira_id)
        return movimentacoes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar movimentações: {str(e)}",
        )
