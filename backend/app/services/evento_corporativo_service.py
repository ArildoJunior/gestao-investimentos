# FILE: backend/app/services/evento_corporativo_service.py
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.evento_corporativo import EventoCorporativo
from app.models.posicao import Posicao
from app.schemas.enums import TipoEventoCorporativo
from app.schemas.evento_corporativo import (
    EventoCorporativoCreate,
    EventoCorporativoRead,
)

OITO_CASAS = Decimal("0.00000001")


def arredondar_pm(valor: Decimal) -> Decimal:
    if not isinstance(valor, Decimal):
        valor = Decimal(str(valor))
    return valor.quantize(OITO_CASAS, rounding=ROUND_HALF_UP)


def registrar_evento_corporativo(
    db: Session,
    data: EventoCorporativoCreate,
) -> EventoCorporativoRead:
    """
    Eventos corporativos são fatos de mercado globais — qualquer
    usuário autenticado pode registrá-los. O isolamento ocorre
    no processamento, onde apenas as posições do usuário são afetadas.
    """
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
    usuario_id: UUID,
) -> EventoCorporativoRead:
    """
    Processa o evento aplicando-o SOMENTE nas posições das carteiras
    que pertencem ao usuário autenticado.
    """
    evento = db.get(EventoCorporativo, evento_id)
    if not evento:
        raise ValueError("Evento corporativo não encontrado.")

    if evento.processado:
        raise ValueError("Evento corporativo já foi processado.")

    # Busca apenas carteiras do usuário autenticado
    carteiras_usuario = (
        db.query(Carteira.id)
        .filter(Carteira.usuario_id == usuario_id)
        .all()
    )
    ids_carteiras = [c.id for c in carteiras_usuario]

    if not ids_carteiras:
        # Usuário não tem carteiras — marca como processado e retorna
        evento.processado = True
        db.commit()
        db.refresh(evento)
        return EventoCorporativoRead.model_validate(evento)

    posicoes = (
        db.query(Posicao)
        .filter(
            Posicao.ativo_id == evento.ativo_id,
            Posicao.carteira_id.in_(ids_carteiras),
        )
        .all()
    )

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


def listar_eventos_corporativos(
    db: Session,
    ativo_id: UUID | None = None,
) -> list[EventoCorporativo]:
    """
    Lista eventos — são dados de mercado públicos entre usuários do sistema,
    portanto sem filtro de usuario_id.
    """
    query = db.query(EventoCorporativo)
    if ativo_id:
        query = query.filter(EventoCorporativo.ativo_id == ativo_id)
    return query.order_by(EventoCorporativo.data_evento.asc()).all()


def _aplicar_evento_na_posicao(
    posicao: Posicao,
    tipo_evento: TipoEventoCorporativo,
    fator: Decimal,
    valor: Decimal | None,
) -> None:
    quantidade_atual = posicao.quantidade
    custo_atual = posicao.custo_total

    if quantidade_atual <= 0:
        return

    if tipo_evento == TipoEventoCorporativo.SPLIT:
        nova_qtd = quantidade_atual * fator
        novo_pm = arredondar_pm(custo_atual / nova_qtd)
        posicao.quantidade = nova_qtd
        posicao.preco_medio = novo_pm
        posicao.custo_total = custo_atual

    elif tipo_evento == TipoEventoCorporativo.GRUPAMENTO:
        if fator == 0:
            raise ValueError("Fator de grupamento não pode ser zero.")
        nova_qtd = quantidade_atual / fator
        novo_pm = arredondar_pm(custo_atual / nova_qtd)
        posicao.quantidade = nova_qtd
        posicao.preco_medio = novo_pm
        posicao.custo_total = custo_atual

    elif tipo_evento == TipoEventoCorporativo.BONIFICACAO:
        if fator <= 1:
            return
        valor_pat = Decimal(str(valor)) if valor is not None else Decimal("0")
        qtd_bonus = quantidade_atual * (fator - Decimal("1"))
        nova_qtd = quantidade_atual + qtd_bonus
        novo_custo = custo_atual + (qtd_bonus * valor_pat)
        novo_pm = arredondar_pm(novo_custo / nova_qtd)
        posicao.quantidade = nova_qtd
        posicao.custo_total = novo_custo
        posicao.preco_medio = novo_pm

    elif tipo_evento == TipoEventoCorporativo.SUBSCRICAO:
        if valor is None:
            raise ValueError(
                "Preço de subscrição (valor) é obrigatório para SUBSCRICAO."
            )
        qtd_subscrita = quantidade_atual * fator
        nova_qtd = quantidade_atual + qtd_subscrita
        novo_custo = custo_atual + (qtd_subscrita * Decimal(str(valor)))
        novo_pm = arredondar_pm(novo_custo / nova_qtd)
        posicao.quantidade = nova_qtd
        posicao.custo_total = novo_custo
        posicao.preco_medio = novo_pm

    elif tipo_evento == TipoEventoCorporativo.AMORTIZACAO:
        if valor is None:
            raise ValueError(
                "Valor amortizado por cota é obrigatório para AMORTIZACAO."
            )
        novo_pm = posicao.preco_medio - Decimal(str(valor))
        if novo_pm < 0:
            novo_pm = Decimal("0")
        novo_pm = arredondar_pm(novo_pm)
        posicao.preco_medio = novo_pm
        posicao.custo_total = novo_pm * quantidade_atual

    else:
        return