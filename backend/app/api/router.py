from fastapi import APIRouter

from app.api import aportes
from app.api import ativos
from app.api import carteiras
from app.api import contas
from app.api import instituicoes
from app.api import movimentacoes
from app.api import posicoes
from app.api import saldos_contas

api_router = APIRouter()

api_router.include_router(instituicoes.router, prefix="/instituicoes", tags=["Instituições"])
api_router.include_router(contas.router, prefix="/contas", tags=["Contas"])
api_router.include_router(ativos.router, prefix="/ativos", tags=["Ativos"])
api_router.include_router(movimentacoes.router, prefix="/movimentacoes", tags=["Movimentações"])
api_router.include_router(posicoes.router, prefix="/posicoes", tags=["Posições"])
api_router.include_router(carteiras.router, prefix="/carteiras", tags=["Carteiras"])
api_router.include_router(aportes.router, prefix="/aportes", tags=["Aportes"])
api_router.include_router(saldos_contas.router, prefix="/saldos-contas", tags=["Saldos Contas"])