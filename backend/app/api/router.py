from __future__ import annotations

from fastapi import APIRouter

from app.api import movimentacoes, posicoes

api_router = APIRouter()
api_router.include_router(movimentacoes.router)
api_router.include_router(posicoes.router)