from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# Diretório base do backend (pasta "backend")
BACKEND_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BACKEND_DIR / ".env"

# Carrega variáveis de ambiente do arquivo .env
load_dotenv(ENV_FILE, override=False)


def _to_bool(value: str | None, default: bool = False) -> bool:
    """Converte string de ambiente em bool de forma tolerante."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    # Banco de dados
    database_url: str = os.getenv("DATABASE_URL", "").strip()

    # Aplicação
    app_name: str = os.getenv("APP_NAME", "Sistema de Investimentos")
    app_env: str = os.getenv("APP_ENV", "development")
    app_debug: bool = _to_bool(os.getenv("APP_DEBUG"), default=True)
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    # CORS / frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")


settings = Settings()

# Fail fast se o banco não estiver configurado
if not settings.database_url:
    raise RuntimeError("DATABASE_URL não configurada no backend/.env")