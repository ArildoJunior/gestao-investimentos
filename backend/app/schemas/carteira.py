# FILE: backend/app/schemas/carteira.py
from __future__ import annotations

from datetime import datetime # Alterado de date para datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict # Importado ConfigDict

# Importa os Enums centralizados para TipoCarteira e ObjetivoCarteira
from app.schemas.enums import TipoCarteira, ObjetivoCarteira


class CarteiraBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=80, description="Nome da carteira")
    # Adicionados campos conforme o modelo de dados do dossiê técnico
    tipo: TipoCarteira = Field(..., description="Tipo da carteira (REAL, TESTE, SIMULADA, ESTRATEGIA)")
    objetivo: ObjetivoCarteira = Field(..., description="Objetivo da carteira (DIVIDENDOS, CRESCIMENTO, etc.)")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição detalhada da carteira") # Tornando opcional e permitindo None
    ativa: bool = Field(True, description="Indica se a carteira está ativa") # Default True
    is_principal: bool = Field(False, description="Indica se é a carteira principal do usuário") # Default False


class CarteiraCreate(CarteiraBase):
    pass


class CarteiraUpdate(BaseModel): # Herda de BaseModel para permitir todos os campos opcionais
    nome: Optional[str] = Field(None, min_length=1, max_length=80, description="Nome da carteira")
    tipo: Optional[TipoCarteira] = Field(None, description="Tipo da carteira (REAL, TESTE, SIMULADA, ESTRATEGIA)")
    objetivo: Optional[ObjetivoCarteira] = Field(None, description="Objetivo da carteira (DIVIDENDOS, CRESCIMENTO, etc.)")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição detalhada da carteira")
    ativa: Optional[bool] = Field(None, description="Indica se a carteira está ativa")
    is_principal: Optional[bool] = Field(None, description="Indica se é a carteira principal do usuário")


class CarteiraRead(CarteiraBase):
    model_config = ConfigDict(from_attributes=True) # Usando ConfigDict para Pydantic v2+

    id: UUID = Field(..., description="ID único da carteira")
    created_at: datetime = Field(..., description="Data e hora de criação do registro") # Corrigido para created_at e datetime
    updated_at: datetime = Field(..., description="Data e hora da última atualização do registro") # Adicionado updated_at