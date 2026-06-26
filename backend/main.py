# FILE: backend/main.py

import logging # Adicione esta linha
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.router import api_router

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Opcional, mas boa prática para o main.py

# ✅ Criar todas as tabelas automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Investimentos",
    description="API para gerenciar investimentos",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    logger.info("Requisição na rota raiz recebida.") # Exemplo de uso do logger
    return {"message": "API Investimentos rodando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)