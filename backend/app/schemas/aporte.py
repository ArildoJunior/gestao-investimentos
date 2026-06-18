from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class AporteBase(BaseModel):
    carteira_id: UUID
    conta_id: UUID
    tipo: str = Field(
        ...,
        description="Tipo de aporte: EXTERNO ou REINVESTIMENTO",
        pattern=r"^(EXTERNO|REINVESTIMENTO)$",
    )
    origem: Optional[str] = Field(
        default=None,
        description=(
            "Origem do aporte, usada principalmente para reinvestimentos: "
            "DIVIDENDO, JCP, RENDIMENTO, JUROS_RF, GANHO_CAPITAL, OUTRO."
        ),
        pattern=r"^(DIVIDENDO|JCP|RENDEIMENTO|JUROS_RF|GANHO_CAPITAL|OUTRO)?$",
    )
    valor: Decimal = Field(..., gt=0)
    data_aporte: date
    movimentacao_id: Optional[UUID] = None
    provento_id: Optional[UUID] = None
    observacao: Optional[str] = None

    @field_validator("valor", mode="before")
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


class AporteRead(BaseModel):
    id: UUID
    carteira_id: UUID
    conta_id: UUID
    tipo: str
    origem: Optional[str]
    valor: Decimal
    data_aporte: date
    movimentacao_id: Optional[UUID]
    provento_id: Optional[UUID]
    observacao: Optional[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True