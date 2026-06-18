from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.movimentacao import Movimentacao, TipoMovimentacao, TipoOperacao
from app.models.posicao import Posicao
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoRead
from app.core.preco_medio import recalcular_posicao


def _calcular_valores_financeiros(
    *,
    quantidade: Decimal,
    preco_unitario: Decimal,
    corretagem: Decimal,
    emolumentos: Decimal,
    iss: Decimal,
    outras_taxas: Decimal,
    tipo_movimentacao: TipoMovimentacao,
) -> tuple[Decimal, Decimal]:
    """
    Calcula valor_bruto e valor_liquido da operação.
    """
    valor_bruto = quantidade * preco_unitario

    custos = (
        (corretagem or Decimal("0"))
        + (emolumentos or Decimal("0"))
        + (iss or Decimal("0"))
        + (outras_taxas or Decimal("0"))
    )

    if tipo_movimentacao == TipoMovimentacao.COMPRA:
        # Compra: valor_liquido = valor_bruto + custos
        valor_liquido = valor_bruto + custos
    else:
        # Venda: valor_liquido = valor_bruto - custos
        valor_liquido = valor_bruto - custos

    return valor_bruto, valor_liquido


def _normalizar_tipo_operacao(valor: str) -> str:
    """
    Mantém compatibilidade de payload legado:
    SWING_TRADE -> SWING
    """
    valor_normalizado = valor.strip().upper()
    if valor_normalizado == "SWING_TRADE":
        return "SWING"
    return valor_normalizado


def registrar_movimentacao(db: Session, dados: MovimentacaoCreate) -> MovimentacaoRead:
    """
    Registra uma movimentação (COMPRA/VENDA) e atualiza a posição correspondente.
    """
    try:
        # 1. Converte strings de entrada em enums
        tipo_mov_enum = TipoMovimentacao(dados.tipo_movimentacao.strip().upper())
        tipo_op_enum = TipoOperacao(_normalizar_tipo_operacao(dados.tipo_operacao))

        # 2. Busca (se existir) a posição atual desse ativo na carteira/conta
        posicao: Posicao | None = (
            db.query(Posicao)
            .filter(
                Posicao.carteira_id == dados.carteira_id,
                Posicao.ativo_id == dados.ativo_id,
                Posicao.conta_id == dados.conta_id,
            )
            .one_or_none()
        )

        if posicao:
            quantidade_atual = posicao.quantidade
            preco_medio_atual = posicao.preco_medio
        else:
            quantidade_atual = Decimal("0")
            preco_medio_atual = Decimal("0")

        # 3. Calcula valores financeiros da operação
        valor_bruto, valor_liquido = _calcular_valores_financeiros(
            quantidade=dados.quantidade,
            preco_unitario=dados.preco_unitario,
            corretagem=dados.corretagem,
            emolumentos=dados.emolumentos,
            iss=dados.iss,
            outras_taxas=dados.outras_taxas,
            tipo_movimentacao=tipo_mov_enum,
        )

        # 4. Recalcula a posição usando o motor de preço médio
        resultado_posicao = recalcular_posicao(
            tipo=tipo_mov_enum.value,  # "COMPRA" ou "VENDA"
            quantidade_atual=quantidade_atual,
            preco_medio_atual=preco_medio_atual,
            quantidade_operacao=dados.quantidade,
            preco_unitario=dados.preco_unitario,
        )

        # 5. Atualiza/cria a posição
        if posicao is None:
            posicao = Posicao(
                carteira_id=dados.carteira_id,
                conta_id=dados.conta_id,
                ativo_id=dados.ativo_id,
                quantidade=resultado_posicao.quantidade,
                preco_medio=resultado_posicao.preco_medio,
                custo_total=resultado_posicao.custo_total,
            )
            db.add(posicao)
        else:
            posicao.quantidade = resultado_posicao.quantidade
            posicao.preco_medio = resultado_posicao.preco_medio
            posicao.custo_total = resultado_posicao.custo_total

        # 6. Cria registro da movimentação
        mov = Movimentacao(
            carteira_id=dados.carteira_id,
            conta_id=dados.conta_id,
            ativo_id=dados.ativo_id,
            tipo=tipo_mov_enum,  # <- nome correto da coluna no model ORM
            tipo_operacao=tipo_op_enum,
            data_operacao=dados.data_operacao,
            data_liquidacao=dados.data_liquidacao,
            quantidade=dados.quantidade,
            preco_unitario=dados.preco_unitario,
            valor_bruto=valor_bruto,
            corretagem=dados.corretagem,
            emolumentos=dados.emolumentos,
            iss=dados.iss,
            outras_taxas=dados.outras_taxas,
            valor_liquido=valor_liquido,
            observacoes=dados.observacoes,
        )

        db.add(mov)
        db.commit()
        db.refresh(mov)
        db.refresh(posicao)

        # 7. Monta a resposta manualmente
        return MovimentacaoRead(
            id=mov.id,
            carteira_id=mov.carteira_id,
            conta_id=mov.conta_id,
            ativo_id=mov.ativo_id,
            tipo_movimentacao=mov.tipo.value,
            tipo_operacao=mov.tipo_operacao.value,
            data_operacao=mov.data_operacao,
            data_liquidacao=mov.data_liquidacao,
            quantidade=mov.quantidade,
            preco_unitario=mov.preco_unitario,
            corretagem=mov.corretagem,
            emolumentos=mov.emolumentos,
            iss=mov.iss,
            outras_taxas=mov.outras_taxas,
            valor_bruto=mov.valor_bruto,
            valor_liquido=mov.valor_liquido,
            observacoes=mov.observacoes,
        )
    except Exception:
        db.rollback()
        raise