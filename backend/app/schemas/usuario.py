# FILE: backend/app/schemas/usuario.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel,ConfigDict, EmailStr, Field

class UsuarioBase(BaseModel):
    email: EmailStr
    nome: str = Field(min_length=1, max_length=255)

class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=8, max_length=255)

class UsuarioInDB(UsuarioBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: EmailStr | None = None