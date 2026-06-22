# FILE: app/schemas/aporte.py
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.schemas.enums import TipoAporte, OrigemAporte # Importações adicionadas

class AporteBase(BaseModel):
    carteira_id: UUID = Field(..., description="ID da carteira à qual o aporte pertence")
    conta_id: UUID = Field(..., description="ID da conta de onde o aporte foi realizado")
    # Alterado de str para TipoAporte e removido pattern
    tipo: TipoAporte = Field(
        ...,
        description="Tipo de aporte: EXTERNO ou REINVESTIMENTO",
    )
    # Alterado de str para OrigemAporte e removido pattern
    origem: Optional[OrigemAporte] = Field(
        default=None,
        description=(
            "Origem do aporte, usada principalmente para reinvestimentos: "
            "DIVIDENDO, JCP, RENDIMENTO, JUROS_RF, GANHO_CAPITAL, OUTRO."
        ),
    )
    valor: Decimal = Field(..., gt=0, description="Valor do aporte")
    data_aporte: date = Field(..., description="Data em que o aporte foi realizado")
    movimentacao_id: Optional[UUID] = Field(None, description="ID da movimentação relacionada, se houver")
    provento_id: Optional[UUID] = Field(None, description="ID do provento relacionado, se houver")
    observacao: Optional[str] = Field(None, max_length=500, description="Observações adicionais sobre o aporte")

    @field_validator("valor", mode="before")
    @classmethod
    def normalizar_valor(cls, v):
        if v is None:
            return v
        if isinstance(v, Decimal):
            return v
        try:
            return Decimal(str(v))
        except Exception as e:
            raise ValueError(f"Valor inválido para campo 'valor': {v}") from e

class AporteCreate(AporteBase):
    """Payload de criação de aporte."""
    pass

class AporteUpdate(BaseModel):
    """Payload para atualização parcial de um aporte existente."""
    carteira_id: Optional[UUID] = Field(None, description="ID da carteira à qual o aporte pertence")
    conta_id: Optional[UUID] = Field(None, description="ID da conta de onde o aporte foi realizado")
    tipo: Optional[TipoAporte] = Field(None, description="Tipo de aporte: EXTERNO ou REINVESTIMENTO")
    origem: Optional[OrigemAporte] = Field(None, description="Origem do aporte, usada principalmente para reinvestimentos")
    valor: Optional[Decimal] = Field(None, gt=0, description="Valor do aporte")
    data_aporte: Optional[date] = Field(None, description="Data em que o aporte foi realizado")
    movimentacao_id: Optional[UUID] = Field(None, description="ID da movimentação relacionada, se houver")
    provento_id: Optional[UUID] = Field(None, description="ID do provento relacionado, se houver")
    observacao: Optional[str] = Field(None, max_length=500, description="Observações adicionais sobre o aporte")

    @field_validator("valor", mode="before")
    @classmethod
    def normalizar_valor(cls, v):
        if v is None:
            return v
        if isinstance(v, Decimal):
            return v
        try:
            return Decimal(str(v))
        except Exception as e:
            raise ValueError(f"Valor inválido para campo 'valor': {v}") from e

class AporteRead(AporteBase):
    """Schema para leitura de um aporte, incluindo campos gerados pelo banco/ORM."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="ID único do aporte")
    created_at: datetime = Field(..., description="Data e hora de criação do registro")
    updated_at: datetime = Field(..., description="Data e hora da última atualização do registro")
