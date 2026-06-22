# FILE: backend/app/core/preco_medio.py
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

def _to_decimal(value: float | int | str | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))

def _round_money(value: Decimal, casas: int = 8) -> Decimal:
    quant = Decimal(10) ** -casas
    return value.quantize(quant, rounding=ROUND_HALF_UP)

@dataclass
class PosicaoResult:
    quantidade: Decimal
    preco_medio: Decimal
    custo_total: Decimal

TipoMovimentacao = Literal["COMPRA", "VENDA"]

def recalcular_posicao(
    *,
    tipo: TipoMovimentacao,
    quantidade_atual: Decimal,
    preco_medio_atual: Decimal,
    quantidade_operacao: Decimal,
    preco_unitario: Decimal,
    custos_operacao: Decimal = Decimal("0"), # <--- NOVO PARÂMETRO: Custos da operação (corretagem, taxas, etc.)
) -> PosicaoResult:
    """
    Recalcula posição de um ativo após uma COMPRA ou VENDA.

    - Sempre trabalha com Decimal.
    - Retorna quantidade, preço médio e custo total atualizados.
    - Inclui custos_operacao no cálculo do preço médio para COMPRAS.
    """

    quantidade_atual = _to_decimal(quantidade_atual)
    preco_medio_atual = _to_decimal(preco_medio_atual)
    quantidade_operacao = _to_decimal(quantidade_operacao)
    preco_unitario = _to_decimal(preco_unitario)
    custos_operacao = _to_decimal(custos_operacao) # <--- Converte para Decimal

    if quantidade_operacao <= 0:
        raise ValueError("quantidade_operacao deve ser > 0")

    if tipo == "COMPRA":
        # Novo custo = custo atual + (qtd_compra * preco_unitario) + custos_operacao
        custo_atual = quantidade_atual * preco_medio_atual
        custo_novo = custo_atual + (quantidade_operacao * preco_unitario) + custos_operacao # <--- Adiciona custos_operacao
        quantidade_nova = quantidade_atual + quantidade_operacao

        if quantidade_nova == 0:
            preco_medio_novo = Decimal("0")
            custo_total_novo = Decimal("0") # Se a quantidade é zero, o custo total também é zero
        else:
            preco_medio_novo = custo_novo / quantidade_nova
            custo_total_novo = custo_novo # O custo total é o custo_novo

        return PosicaoResult(
            quantidade=_round_money(quantidade_nova, 8),
            preco_medio=_round_money(preco_medio_novo, 8),
            custo_total=_round_money(custo_total_novo, 8), # Retorna o custo total calculado
        )

    elif tipo == "VENDA":
        if quantidade_operacao > quantidade_atual:
            raise ValueError(
                "Não é permitido vender mais do que a quantidade em posição."
            )

        quantidade_nova = quantidade_atual - quantidade_operacao

        # Na venda, o preço médio não muda, a menos que a posição seja zerada.
        if quantidade_nova == 0:
            preco_medio_novo = Decimal("0")
            custo_total_novo = Decimal("0")
        else:
            preco_medio_novo = preco_medio_atual
            custo_total_novo = quantidade_nova * preco_medio_atual # Custo total atualizado

        return PosicaoResult(
            quantidade=_round_money(quantidade_nova, 8),
            preco_medio=_round_money(preco_medio_novo, 8),
            custo_total=_round_money(custo_total_novo, 8), # Retorna o custo total atualizado
        )

    else:
        raise ValueError(f"Tipo de movimentação não suportado: {tipo}")