# FILE: backend/app/services/movimentacao_service.py
from __future__ import annotations

from decimal import Decimal
from typing import List # Importação adicionada
from uuid import UUID # Importação adicionada

from sqlalchemy.orm import Session

from app.core.preco_medio import recalcular_posicao
from app.models.movimentacao import Movimentacao
from app.models.posicao import Posicao
from app.schemas.enums import TipoMovimentacao, TipoOperacao
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoRead


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
    valor_bruto = quantidade * preco_unitario

    custos = (
        (corretagem or Decimal("0"))
        + (emolumentos or Decimal("0"))
        + (iss or Decimal("0"))
        + (outras_taxas or Decimal("0"))
    )

    if tipo_movimentacao == TipoMovimentacao.COMPRA:
        valor_liquido = valor_bruto + custos
    else:
        valor_liquido = valor_bruto - custos

    return valor_bruto, valor_liquido


def _parse_tipo_movimentacao(value: TipoMovimentacao | str) -> TipoMovimentacao:
    if isinstance(value, TipoMovimentacao):
        return value
    return TipoMovimentacao(value.strip().upper())


def _parse_tipo_operacao(value: TipoOperacao | str) -> TipoOperacao:
    if isinstance(value, TipoOperacao):
        return value
    raw = value.strip().upper()
    if raw == "SWING_TRADE":
        raw = "SWING"
    return TipoOperacao(raw)


def registrar_movimentacao(db: Session, dados: MovimentacaoCreate) -> MovimentacaoRead:
    try:
        tipo_mov_enum = _parse_tipo_movimentacao(dados.tipo_movimentacao)
        tipo_op_enum = _parse_tipo_operacao(dados.tipo_operacao)

        posicao: Posicao | None = (
            db.query(Posicao)
            .filter(
                Posicao.carteira_id == dados.carteira_id,
                Posicao.ativo_id == dados.ativo_id,
                Posicao.conta_id == dados.conta_id,
            )
            .one_or_none()
        )

        quantidade_atual = posicao.quantidade if posicao else Decimal("0")
        preco_medio_atual = posicao.preco_medio if posicao else Decimal("0")

        valor_bruto, valor_liquido = _calcular_valores_financeiros(
            quantidade=dados.quantidade,
            preco_unitario=dados.preco_unitario,
            corretagem=dados.corretagem,
            emolumentos=dados.emolumentos,
            iss=dados.iss,
            outras_taxas=dados.outras_taxas,
            tipo_movimentacao=tipo_mov_enum,
        )

        custos_operacao = (
            (dados.corretagem or Decimal("0"))
            + (dados.emolumentos or Decimal("0"))
            + (dados.iss or Decimal("0"))
            + (dados.outras_taxas or Decimal("0"))
        )

        resultado_posicao = recalcular_posicao(
            tipo=tipo_mov_enum.value,
            quantidade_atual=quantidade_atual,
            preco_medio_atual=preco_medio_atual,
            quantidade_operacao=dados.quantidade,
            preco_unitario=dados.preco_unitario,
            custos_operacao=custos_operacao if tipo_mov_enum == TipoMovimentacao.COMPRA else Decimal("0"),
        )

        if resultado_posicao.quantidade <= Decimal("0"):
            if posicao is not None:
                db.delete(posicao)
        else:
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

        mov = Movimentacao(
            carteira_id=dados.carteira_id,
            conta_id=dados.conta_id,
            ativo_id=dados.ativo_id,
            tipo_movimentacao=tipo_mov_enum,
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

        return MovimentacaoRead.model_validate(mov)
    except ValueError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise RuntimeError("Erro interno ao registrar movimentação.") from exc


def listar_movimentacoes_por_carteira(
    db: Session, carteira_id: UUID, skip: int = 0, limit: int = 100
) -> List[MovimentacaoRead]:
    """
    Lista todas as movimentações para uma carteira específica.
    """
    movimentacoes = (
        db.query(Movimentacao)
        .filter(Movimentacao.carteira_id == carteira_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [MovimentacaoRead.model_validate(mov) for mov in movimentacoes]
