from __future__ import annotations

from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(title="Investimentos API")

app.include_router(api_router, prefix="/api")