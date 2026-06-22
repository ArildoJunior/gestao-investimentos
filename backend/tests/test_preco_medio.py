# FILE NAME: test_preco_medio.py
from decimal import Decimal
import pytest
from app.core.preco_medio import recalcular_posicao, PosicaoResult

def test_compra_inicial():
    """
    Testa a compra inicial de um ativo.
    """
    resultado = recalcular_posicao(
        quantidade_atual=Decimal("0"),
        preco_medio_atual=Decimal("0"),
        quantidade_operacao=Decimal("100"),
        preco_unitario=Decimal("10"),
        tipo="COMPRA",
    )

    assert isinstance(resultado, PosicaoResult)
    assert resultado.quantidade == Decimal("100.00000000")
    assert resultado.preco_medio == Decimal("10.00000000")
    assert resultado.custo_total == Decimal("1000.00000000")

def test_compra_adicional():
    """
    Testa a compra de um ativo que já possui posição.
    """
    # Posição atual: 100 unidades a R$10,00 (Custo total: R$1000,00)
    # Nova compra: 50 unidades a R$12,00 (Custo da operação: R$600,00)
    # Custo total esperado: R$1000 + R$600 = R$1600,00
    # Quantidade esperada: 100 + 50 = 150
    # Preço médio esperado: R$1600 / 150 = R$10,66666667
    resultado = recalcular_posicao(
        quantidade_atual=Decimal("100"),
        preco_medio_atual=Decimal("10"),
        quantidade_operacao=Decimal("50"),
        preco_unitario=Decimal("12"),
        tipo="COMPRA",
    )

    assert isinstance(resultado, PosicaoResult)
    assert resultado.quantidade == Decimal("150.00000000")
    assert resultado.preco_medio == Decimal("10.66666667")
    assert resultado.custo_total == Decimal("1600.00000000")

def test_venda_parcial():
    """
    Testa a venda parcial de um ativo.
    O preço médio não deve mudar.
    """
    # Posição atual: 100 unidades a R$10,00 (Custo total: R$1000,00)
    # Venda: 30 unidades a R$15,00 (Preço de venda não afeta o preço médio)
    # Quantidade esperada: 100 - 30 = 70
    # Preço médio esperado: R$10,00 (não muda)
    # Custo total esperado: 70 * R$10,00 = R$700,00
    resultado = recalcular_posicao(
        quantidade_atual=Decimal("100"),
        preco_medio_atual=Decimal("10"),
        quantidade_operacao=Decimal("30"),
        preco_unitario=Decimal("15"), # Preço de venda não afeta o preço médio
        tipo="VENDA",
    )

    assert isinstance(resultado, PosicaoResult)
    assert resultado.quantidade == Decimal("70.00000000")
    assert resultado.preco_medio == Decimal("10.00000000")
    assert resultado.custo_total == Decimal("700.00000000")

def test_venda_total():
    """
    Testa a venda total de um ativo.
    """
    # Posição atual: 100 unidades a R$10,00 (Custo total: R$1000,00)
    # Venda: 100 unidades a R$15,00
    # Quantidade esperada: 0
    # Preço médio esperado: 0
    # Custo total esperado: 0
    resultado = recalcular_posicao(
        quantidade_atual=Decimal("100"),
        preco_medio_atual=Decimal("10"),
        quantidade_operacao=Decimal("100"),
        preco_unitario=Decimal("15"),
        tipo="VENDA",
    )

    assert isinstance(resultado, PosicaoResult)
    assert resultado.quantidade == Decimal("0.00000000")
    assert resultado.preco_medio == Decimal("0.00000000")
    assert resultado.custo_total == Decimal("0.00000000")

def test_venda_maior_que_posicao_levanta_erro():
    """
    Testa se tentar vender mais do que a posição atual levanta um ValueError.
    """
    with pytest.raises(ValueError, match="Não é permitido vender mais do que a quantidade em posição."):
        recalcular_posicao(
            quantidade_atual=Decimal("100"),
            preco_medio_atual=Decimal("10"),
            quantidade_operacao=Decimal("101"),
            preco_unitario=Decimal("15"),
            tipo="VENDA",
        )

def test_operacao_com_quantidade_zero_levanta_erro():
    """
    Testa se uma operação com quantidade zero levanta um ValueError.
    """
    with pytest.raises(ValueError, match="quantidade_operacao deve ser > 0"):
        recalcular_posicao(
            quantidade_atual=Decimal("100"),
            preco_medio_atual=Decimal("10"),
            quantidade_operacao=Decimal("0"),
            preco_unitario=Decimal("15"),
            tipo="COMPRA",
        )

def test_operacao_com_quantidade_negativa_levanta_erro():
    """
    Testa se uma operação com quantidade negativa levanta um ValueError.
    """
    with pytest.raises(ValueError, match="quantidade_operacao deve ser > 0"):
        recalcular_posicao(
            quantidade_atual=Decimal("100"),
            preco_medio_atual=Decimal("10"),
            quantidade_operacao=Decimal("-10"),
            preco_unitario=Decimal("15"),
            tipo="COMPRA",
        )

def test_precisao_decimal_compra():
    """
    Testa a precisão decimal em uma compra com valores complexos.
    """
    # Posição atual: 10 unidades a R$1.23456789 (Custo: R$12.34567890)
    # Nova compra: 7 unidades a R$2.34567891 (Custo: R$16.41975237)
    # Custo total esperado: R$12.34567890 + R$16.41975237 = R$28.76543127
    # Quantidade esperada: 10 + 7 = 17
    # Preço médio esperado: R$28.76543127 / 17 = R$1.69208419
    resultado = recalcular_posicao(
        quantidade_atual=Decimal("10"),
        preco_medio_atual=Decimal("1.23456789"),
        quantidade_operacao=Decimal("7"),
        preco_unitario=Decimal("2.34567891"),
        tipo="COMPRA",
    )
    assert resultado.quantidade == Decimal("17.00000000")
    assert resultado.preco_medio == Decimal("1.69208419")
    assert resultado.custo_total == Decimal("28.76543127")

def test_precisao_decimal_venda():
    """
    Testa a precisão decimal em uma venda com valores complexos.
    """
    # Posição atual: 17 unidades a R$1.69208419 (Custo: R$28.76543123)
    # Venda: 5 unidades a R$3.00000000
    # Quantidade esperada: 17 - 5 = 12
    # Preço médio esperado: R$1.69208419 (não muda)
    # Custo total esperado: 12 * R$1.69208419 = R$20.30501028
    resultado = recalcular_posicao(
        quantidade_atual=Decimal("17"),
        preco_medio_atual=Decimal("1.69208419"),
        quantidade_operacao=Decimal("5"),
        preco_unitario=Decimal("3.00000000"),
        tipo="VENDA",
    )
    assert resultado.quantidade == Decimal("12.00000000")
    assert resultado.preco_medio == Decimal("1.69208419")
    assert resultado.custo_total == Decimal("20.30501028")
