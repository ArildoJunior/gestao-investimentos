from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoRead
from app.services.movimentacao_service import registrar_movimentacao

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