from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.enums import TipoEventoCorporativo


class EventoCorporativoBase(BaseModel):
    ativo_id: UUID = Field(..., description="Ativo de origem do evento")
    tipo: TipoEventoCorporativo
    data_evento: date
    fator: Decimal = Field(..., gt=0, description="Fator do evento (ex: 2 para split 1:2)")
    valor: Decimal | None = Field(
        None,
        description="Valor por cota (amortização, bonificação com valor patrimonial, etc.)",
    )
    ativo_destino_id: UUID | None = Field(
        None,
        description="Ativo destino (em incorporações/fusões/cisões, se aplicável)",
    )
    observacoes: str | None = None

    @field_validator("fator", "valor", mode="before")
    def normalizar_decimal(cls, v):
        from decimal import Decimal as _D

        if v is None:
            return v
        if isinstance(v, _D):
            return v
        try:
            return _D(str(v))
        except Exception as e:
            raise ValueError(f"Valor numérico inválido: {v}") from e


class EventoCorporativoCreate(EventoCorporativoBase):
    """
    Payload de criação de evento corporativo.
    """
    pass


class EventoCorporativoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ativo_id: UUID
    tipo: TipoEventoCorporativo
    data_evento: date
    fator: Decimal
    valor: Decimal | None
    ativo_destino_id: UUID | None
    observacoes: str | None
    processado: bool
    created_at: datetime
    updated_at: datetime