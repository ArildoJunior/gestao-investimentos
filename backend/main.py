# FILE: backend/main.py

from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="Sistema de Controle de Investimentos e Patrimônio",
    description="API para gestão de ativos, movimentações, carteiras e cálculos financeiros.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Router principal da API
app.include_router(api_router, prefix="/api")


@app.get("/api/health", tags=["Health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Bem-vindo à API de Controle de Investimentos!"}