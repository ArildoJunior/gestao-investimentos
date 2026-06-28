# FILE: backend/main.py
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.router import api_router
from app.api.auth import auth_router
from app.config import settings  # corrigido: era app.core.config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Investimentos",
    description="Sistema de controle de investimentos pessoais",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# auth_router registrado UMA única vez, fora do api_router
app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticação"])


@app.get("/", tags=["Health"])
def read_root():
    logger.info("Requisição na rota raiz recebida.")
    return {"message": "API Investimentos rodando!", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=settings.app_port)