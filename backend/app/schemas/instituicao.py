# FILE: backend/app/schemas/instituicao.py
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.enums import StatusInstituicao, TipoInstituicao # Importa os Enums centralizados

# Schema base para Instituicao (campos comuns)
class InstituicaoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255, description="Nome da instituição")
    tipo: TipoInstituicao = Field(..., description="Tipo da instituição (CORRETORA, BANCO, OUTRO)")
    status: StatusInstituicao = Field(
        StatusInstituicao.ATIVA, description="Status da instituição (ATIVO, INATIVO)" # Use o membro do Enum diretamente
    )

# Schema para criação de Instituicao
class InstituicaoCreate(InstituicaoBase):
    pass

# Schema para atualização de Instituicao
class InstituicaoUpdate(BaseModel): # Herda de BaseModel para permitir todos os campos opcionais
    nome: Optional[str] = Field(None, min_length=3, max_length=255, description="Nome da instituição")
    tipo: Optional[TipoInstituicao] = Field(None, description="Tipo da instituição (CORRETORA, BANCO, OUTRO)")
    status: Optional[StatusInstituicao] = Field(None, description="Status da instituição (ATIVO, INATIVO)")

# Schema para leitura de Instituicao (inclui campos gerados pelo banco/ORM)
class InstituicaoRead(InstituicaoBase): # Renomeado para InstituicaoRead para consistência
    model_config = ConfigDict(from_attributes=True) # Adicionado para Pydantic v2+

    id: UUID = Field(..., description="ID único da instituição")
    created_at: datetime = Field(..., description="Data e hora de criação do registro")
    updated_at: datetime = Field(..., description="Data e hora da última atualização do registro")