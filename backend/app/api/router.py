# FILE: backend/app/api/router.py

from fastapi import APIRouter

# Importe os routers de cada módulo
from app.api import instituicoes
from app.api import contas
from app.api import ativos
from app.api import movimentacoes
from app.api import posicoes
from app.api import carteiras
from app.api import aportes # Adicionado import para aportes

api_router = APIRouter()

# Inclua os routers com seus respectivos prefixos e tags
api_router.include_router(instituicoes.router, prefix="/instituicoes", tags=["Instituições"])
api_router.include_router(contas.router, prefix="/contas", tags=["Contas"])
api_router.include_router(ativos.router, prefix="/ativos", tags=["Ativos"])
api_router.include_router(movimentacoes.router, prefix="/movimentacoes", tags=["Movimentações"])
api_router.include_router(posicoes.router, prefix="/posicoes", tags=["Posições"])
api_router.include_router(carteiras.router, prefix="/carteiras", tags=["Carteiras"])
api_router.include_router(aportes.router, prefix="/aportes", tags=["Aportes"]) # Adicionado router de aportes
