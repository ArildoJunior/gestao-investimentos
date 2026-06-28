# FILE: backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configurações do Banco de Dados
    database_url: str

    # Configurações da Aplicação
    app_name: str = "Sistema de Investimentos"
    app_env: str = "development"
    app_debug: bool = False
    app_port: int = 8000

    # Configurações CORS
    frontend_url: str

    # Configurações de Autenticação JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30  # Tempo de expiração do token em minutos

    # Configurações de APIs Externas (mantidas do .env original)
    brapi_token: str | None = None
    bcb_api_url: str = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
    tesouro_url: str = "https://www.tesourodireto.com.br/json/br/com/b3/tesouro/bond/jsonBonds.json"

    # Configurações do Agendador (mantidas do .env original)
    scheduler_enabled: bool = True
    horario_cotacoes_b3: str = "18:30"
    horario_cotacoes_ext: str = "18:30"
    horario_benchmarks: str = "19:00"
    horario_snapshot: str = "23:59"
    horario_alertas: str = "08:00"
    horario_fundamentalistas: str = "06:00"

    # Limites Tributários (mantidos do .env original)
    limite_isencao_acoes: float = 20000.00
    limite_isencao_cripto: float = 35000.00

    # Alertas (mantidos do .env original)
    alerta_isentometro_warning: int = 70
    alerta_isentometro_critico: int = 90
    alerta_rebalanceamento_warning: int = 5
    alerta_rebalanceamento_critico: int = 10
    alerta_vencimento_dias: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()