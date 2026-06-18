from app.core.preco_medio import recalcular_posicao, PosicaoResult

def test_compra_inicial():
    resultado = recalcular_posicao(
        quantidade_atual=0,
        preco_medio_atual=0,
        quantidade_operacao=100,
        preco_unitario=10,
        tipo="COMPRA",
    )

    assert isinstance(resultado, PosicaoResult)
    assert resultado.quantidade == 100
    assert resultado.preco_medio == 10
    assert resultado.custo_total == 1000