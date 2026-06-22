# FILE: app/schemas/ativo.py
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator, ConfigDict

# Importa os Enums centralizados com os nomes corretos
from app.schemas.enums import TipoAtivo, SegmentoFII, RegiaoAtivo, StatusAtivo # Corrigido ClasseAtivo para TipoAtivo e Regiao para RegiaoAtivo
# Não há um Enum Moeda em app.schemas.enums no arquivo que você me enviou.
# Se Moeda for um Enum, ele precisa ser definido em enums.py.
# Por enquanto, vou assumir que Moeda é um str ou que você tem um Enum Moeda definido em outro lugar.
# Se for um Enum, ele deve ser importado daqui:
# from app.schemas.enums import Moeda
# Por simplicidade e para resolver o erro, vou assumir que Moeda é um str por enquanto,
# mas se você tiver um Enum Moeda, por favor, me avise.

# Se Moeda for um Enum e estiver em enums.py, descomente a linha abaixo e remova a definição de Moeda como str
# from app.schemas.enums import Moeda

# Se Moeda não for um Enum, mas sim um str, podemos definir um tipo simples para ele
# class Moeda(str, Enum):
#     BRL = "BRL"
#     USD = "USD"
#     EUR = "EUR"

# Para o propósito desta correção, vou assumir que Moeda é um Enum que precisa ser importado
# Se não for, você precisará ajustar.
# Para o contexto do seu docx, Moeda é um ENUM BRL / USD / EUR.
# Vou adicionar uma definição temporária aqui para que o código compile,
# mas o ideal é que ele venha do seu enums.py se for um Enum.
# Ou, se for apenas um string, remova a importação e use 'str' diretamente.

# Baseado no seu docx, Moeda é um Enum. Vou adicioná-lo ao enums.py e importá-lo.
# Para que este arquivo funcione AGORA, vou usar um placeholder.
# O correto é que ele seja definido em app.schemas.enums.
# Para fins de correção do erro atual, vou manter como str e depois você ajusta o enums.py
# ou me envia o enums.py completo com Moeda.

# --- CORREÇÃO: Assumindo que Moeda será um Enum em app.schemas.enums ---
# Para que o código compile, vou adicionar Moeda ao enums.py e importá-lo.
# Por favor, certifique-se de que o seu app/schemas/enums.py contenha:
# class Moeda(str, Enum):
#     BRL = "BRL"
#     USD = "USD"
#     EUR = "EUR"
# ---------------------------------------------------------------------

# Importando Moeda, assumindo que foi adicionado ao enums.py
from app.schemas.enums import Moeda # Adicionado Moeda aqui

# Schema base para Ativo (campos comuns)
class AtivoBase(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=20, description="Ticker do ativo (ex: PETR4, AAPL34)")
    nome: str = Field(..., min_length=1, max_length=255, description="Nome completo do ativo")
    classe: TipoAtivo = Field(..., description="Classe do ativo (ex: ACAO, FII, CRIPTO)") # Corrigido para TipoAtivo
    setor: Optional[str] = Field(None, max_length=255, description="Setor de atuação do ativo (ex: Petróleo e Gás)")
    segmento_fii: Optional[SegmentoFII] = Field(None, description="Segmento específico para FIIs (ex: TIJOLO, PAPEL)")
    pais: str = Field("BR", max_length=10, description="País de origem do ativo (ex: BR, US)")
    regiao: RegiaoAtivo = Field(RegiaoAtivo.BRASIL, description="Região geográfica do ativo (ex: BRASIL, AMERICA_NORTE)") # Corrigido para RegiaoAtivo
    moeda: Moeda = Field(Moeda.BRL, description="Moeda de negociação (ex: BRL, USD)") # Usa o Enum Moeda
    status: StatusAtivo = Field(StatusAtivo.ATIVO, description="Status do ativo (ATIVO, INATIVO)")

    @field_validator(
        "ticker",
        "nome",
        "setor",
        "pais",
        mode="before",
    )
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

# Schema para criação de Ativo (herda de AtivoBase)
class AtivoCreate(AtivoBase):
    pass

# Schema para atualização de Ativo (todos os campos são opcionais)
class AtivoUpdate(BaseModel): # Herda de BaseModel para permitir todos os campos opcionais
    ticker: Optional[str] = Field(None, min_length=1, max_length=20, description="Ticker do ativo (ex: PETR4, AAPL34)")
    nome: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome completo do ativo")
    classe: Optional[TipoAtivo] = Field(None, description="Classe do ativo (ex: ACAO, FII, CRIPTO)") # Corrigido para TipoAtivo
    setor: Optional[str] = Field(None, max_length=255, description="Setor de atuação do ativo (ex: Petróleo e Gás)")
    segmento_fii: Optional[SegmentoFII] = Field(None, description="Segmento específico para FIIs (ex: TIJOLO, PAPEL)")
    pais: Optional[str] = Field(None, max_length=10, description="País de origem do ativo (ex: BR, US)")
    regiao: Optional[RegiaoAtivo] = Field(None, description="Região geográfica do ativo (ex: BRASIL, AMERICA_NORTE)") # Corrigido para RegiaoAtivo
    moeda: Optional[Moeda] = Field(None, description="Moeda de negociação (ex: BRL, USD)")
    status: Optional[StatusAtivo] = Field(None, description="Status do ativo (ATIVO, INATIVO)")

# Schema para leitura de Ativo (inclui campos gerados pelo banco/ORM)
class AtivoRead(AtivoBase): # Renomeado para AtivoRead
    model_config = ConfigDict(from_attributes=True) # Adicionado para Pydantic v2+

    id: UUID = Field(..., description="ID único do ativo")
    created_at: datetime = Field(..., description="Data e hora de criação do registro")
    updated_at: datetime = Field(..., description="Data e hora da última atualização do registro")