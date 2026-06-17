from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.preco_medio import recalcular_posicao
from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.movimentacao import Movimentacao, TipoMovimentacao
from app.models.posicao import Posicao
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoRead


def _calcular_valores_financeiros(
    quantidade: Decimal,
    preco_unitario: Decimal,
    corretagem: Decimal,
    emolumentos: Decimal,
    iss: Decimal,
    outras_taxas: Decimal,
    tipo_movimentacao: TipoMovimentacao,
) -> tuple[Decimal, Decimal]:
    valor_bruto = quantidade * preco_unitario
    custos = corretagem + emolumentos + iss + outras_taxas

    if tipo_movimentacao == TipoMovimentacao.COMPRA:
        valor_liquido = valor_bruto + custos
    else:
        # VENDA: custos diminuem o líquido recebido
        valor_liquido = valor_bruto - custos

    return valor_bruto, valor_liquido


def registrar_movimentacao(db: Session, data: MovimentacaoCreate) -> MovimentacaoRead:
    """
    Registra uma compra/venda, atualiza posição e retorna a movimentação.
    """

    # 1. Garantir que carteira, ativo e conta (se enviada) existem
    carteira = db.get(Carteira, data.carteira_id)
    if carteira is None:
        raise ValueError("Carteira não encontrada.")

    ativo = db.get(Ativo, data.ativo_id)
    if ativo is None:
        raise ValueError("Ativo não encontrado.")

    conta: Conta | None = None
    if data.conta_id is not None:
        conta = db.get(Conta, data.conta_id)
        if conta is None:
            raise ValueError("Conta não encontrada.")

    # 2. Buscar (ou criar) posição existente
    stmt = select(Posicao).where(
        Posicao.carteira_id == data.carteira_id,
        Posicao.ativo_id == data.ativo_id,
        Posicao.conta_id.is_(data.conta_id) if data.conta_id is None else Posicao.conta_id == data.conta_id,
    )
    posicao = db.scalar(stmt)

    quantidade_atual = posicao.quantidade if posicao else Decimal("0")
    preco_medio_atual = posicao.preco_medio if posicao else Decimal("0")

    # 3. Calcular valores da movimentação
    valor_bruto, valor_liquido = _calcular_valores_financeiros(
        quantidade=data.quantidade,
        preco_unitario=data.preco_unitario,
        corretagem=data.corretagem,
        emolumentos=data.emolumentos,
        iss=data.iss,
        outras_taxas=data.outras_taxas,
        tipo_movimentacao=TipoMovimentacao(data.tipo_movimentacao),
    )

    # 4. Recalcular posição
    resultado_posicao = recalcular_posicao(
        tipo=data.tipo_movimentacao,  # "COMPRA" ou "VENDA"
        quantidade_atual=quantidade_atual,
        preco_medio_atual=preco_medio_atual,
        quantidade_operacao=data.quantidade,
        preco_unitario=data.preco_unitario,
    )

    # 5. Atualizar/criar posição
    if posicao is None:
        posicao = Posicao(
            carteira_id=data.carteira_id,
            conta_id=data.conta_id,
            ativo_id=data.ativo_id,
            quantidade=resultado_posicao.quantidade,
            preco_medio=resultado_posicao.preco_medio,
            custo_total=resultado_posicao.custo_total,
        )
        db.add(posicao)
    else:
        posicao.quantidade = resultado_posicao.quantidade
        posicao.preco_medio = resultado_posicao.preco_medio
        posicao.custo_total = resultado_posicao.custo_total

    # 6. Criar registro de movimentação
    mov = Movimentacao(
        carteira_id=data.carteira_id,
        conta_id=data.conta_id,
        ativo_id=data.ativo_id,
        tipo_movimentacao=TipoMovimentacao(data.tipo_movimentacao),
        tipo_operacao=data.tipo_operacao,
        data_operacao=data.data_operacao,
        data_liquidacao=data.data_liquidacao,
        quantidade=data.quantidade,
        preco_unitario=data.preco_unitario,
        valor_bruto=valor_bruto,
        corretagem=data.corretagem,
        emolumentos=data.emolumentos,
        iss=data.iss,
        outras_taxas=data.outras_taxas,
        valor_liquido=valor_liquido,
        observacoes=data.observacoes,
    )
    db.add(mov)

    db.commit()
    db.refresh(mov)
    db.refresh(posicao)

    # 7. Retornar schema de leitura
    return MovimentacaoRead.model_validate(mov)