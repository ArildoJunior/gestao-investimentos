from fastapi import APIRouter

from app.api import movimentacoes, posicoes, aportes, proventos

api_router = APIRouter()
api_router.include_router(movimentacoes.router)
api_router.include_router(posicoes.router)
api_router.include_router(aportes.router)
api_router.include_router(proventos.router)