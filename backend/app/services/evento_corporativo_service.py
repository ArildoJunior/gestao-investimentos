from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.evento_corporativo import EventoCorporativo
from app.models.posicao import Posicao
from app.schemas.enums import TipoEventoCorporativo
from app.schemas.evento_corporativo import (
    EventoCorporativoCreate,
    EventoCorporativoRead,
)

OITO_CASAS = Decimal("0.00000001")
QUATRO_CASAS = Decimal("0.0001")


def arredondar_pm(valor: Decimal) -> Decimal:
    if not isinstance(valor, Decimal):
        valor = Decimal(str(valor))
    return valor.quantize(OITO_CASAS, rounding=ROUND_HALF_UP)


def registrar_evento_corporativo(
    db: Session,
    data: EventoCorporativoCreate,
) -> EventoCorporativoRead:
    ativo = db.get(Ativo, data.ativo_id)
    if not ativo:
        raise ValueError("Ativo não encontrado para o evento corporativo.")

    evento = EventoCorporativo(
        ativo_id=data.ativo_id,
        tipo=data.tipo,
        data_evento=data.data_evento,
        fator=data.fator,
        valor=data.valor,
        ativo_destino_id=data.ativo_destino_id,
        observacoes=data.observacoes,
        processado=False,
    )

    db.add(evento)
    db.commit()
    db.refresh(evento)

    return EventoCorporativoRead.model_validate(evento)


def processar_evento_corporativo(
    db: Session,
    evento_id: UUID,
) -> EventoCorporativoRead:
    evento = db.get(EventoCorporativo, evento_id)
    if not evento:
        raise ValueError("Evento corporativo não encontrado.")

    if evento.processado:
        raise ValueError("Evento corporativo já foi processado.")

    posicoes = (
        db.query(Posicao)
        .filter(Posicao.ativo_id == evento.ativo_id)
        .all()
    )

    if not posicoes:
        evento.processado = True
        db.commit()
        db.refresh(evento)
        return EventoCorporativoRead.model_validate(evento)

    for posicao in posicoes:
        _aplicar_evento_na_posicao(
            posicao=posicao,
            tipo_evento=evento.tipo,
            fator=evento.fator,
            valor=evento.valor,
        )

    evento.processado = True
    db.commit()
    db.refresh(evento)

    return EventoCorporativoRead.model_validate(evento)


def _aplicar_evento_na_posicao(
    posicao: Posicao,
    tipo_evento: TipoEventoCorporativo,
    fator: Decimal,
    valor: Decimal | None,
) -> None:
    quantidade_atual = posicao.quantidade
    pm_atual = posicao.preco_medio
    custo_atual = posicao.custo_total

    if quantidade_atual <= 0:
        return

    if tipo_evento == TipoEventoCorporativo.SPLIT:
        # custo_total é preservado; pm é derivado do custo
        nova_qtd = quantidade_atual * fator
        novo_custo = custo_atual  # split não altera custo financeiro
        novo_pm = arredondar_pm(novo_custo / nova_qtd)
        posicao.quantidade = nova_qtd
        posicao.preco_medio = novo_pm
        posicao.custo_total = novo_custo

    elif tipo_evento == TipoEventoCorporativo.GRUPAMENTO:
        if fator == 0:
            raise ValueError("Fator de grupamento não pode ser zero.")
        # custo_total é preservado; pm é derivado do custo
        nova_qtd = quantidade_atual / fator
        novo_custo = custo_atual  # grupamento não altera custo financeiro
        novo_pm = arredondar_pm(novo_custo / nova_qtd)
        posicao.quantidade = nova_qtd
        posicao.preco_medio = novo_pm
        posicao.custo_total = novo_custo

    elif tipo_evento == TipoEventoCorporativo.BONIFICACAO:
        if fator <= 1:
            return

        valor_pat = Decimal(str(valor)) if valor is not None else Decimal("0")

        qtd_bonus = quantidade_atual * (fator - Decimal("1"))
        custo_bonus = qtd_bonus * valor_pat
        nova_qtd = quantidade_atual + qtd_bonus
        # custo_total calculado diretamente — pm é derivado DEPOIS
        novo_custo = custo_atual + custo_bonus
        novo_pm = arredondar_pm(novo_custo / nova_qtd)

        posicao.quantidade = nova_qtd
        posicao.custo_total = novo_custo   # fonte da verdade
        posicao.preco_medio = novo_pm      # derivado

    elif tipo_evento == TipoEventoCorporativo.SUBSCRICAO:
        if valor is None:
            raise ValueError(
                "Preço de subscrição (valor) é obrigatório para SUBSCRICAO."
            )

        qtd_subscrita = quantidade_atual * fator
        custo_subscricao = qtd_subscrita * Decimal(str(valor))
        nova_qtd = quantidade_atual + qtd_subscrita
        # custo_total calculado diretamente — pm é derivado DEPOIS
        novo_custo = custo_atual + custo_subscricao
        novo_pm = arredondar_pm(novo_custo / nova_qtd)

        posicao.quantidade = nova_qtd
        posicao.custo_total = novo_custo   # fonte da verdade
        posicao.preco_medio = novo_pm      # derivado

    elif tipo_evento == TipoEventoCorporativo.AMORTIZACAO:
        if valor is None:
            raise ValueError(
                "Valor amortizado por cota é obrigatório para AMORTIZACAO."
            )

        novo_pm = pm_atual - Decimal(str(valor))
        if novo_pm < 0:
            novo_pm = Decimal("0")

        novo_pm = arredondar_pm(novo_pm)
        # aqui custo_total é derivado do pm porque a amortização
        # age diretamente sobre o preço por cota
        posicao.preco_medio = novo_pm
        posicao.custo_total = novo_pm * quantidade_atual

    else:
        return