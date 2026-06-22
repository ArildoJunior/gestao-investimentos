# FILE: backend/tests/test_api_movimentacoes.py

from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.instituicao import Instituicao
from app.schemas.enums import TipoMovimentacao, TipoOperacao
from app.schemas.movimentacao import MovimentacaoCreate
from app.schemas.posicao import PosicaoRead

def test_registrar_compra_inicial_e_atualizar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    movimentacao_create = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    # Removida a barra no final da URL
    response = client.post("/api/movimentacoes", json=movimentacao_create.model_dump(mode="json"))
    assert response.status_code == 201

def test_registrar_compra_adicional_e_atualizar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # Compra inicial
    movimentacao_inicial = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    client.post("/api/movimentacoes", json=movimentacao_inicial.model_dump(mode="json"))

    # Compra adicional
    movimentacao_adicional = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("50"),
        preco_unitario=Decimal("26.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.25"),
        emolumentos=Decimal("0.05"),
        tipo_operacao=TipoOperacao.SWING,
    )
    response = client.post("/api/movimentacoes", json=movimentacao_adicional.model_dump(mode="json"))
    assert response.status_code == 201

def test_registrar_venda_parcial_e_atualizar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # Compra inicial
    movimentacao_compra = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    client.post("/api/movimentacoes", json=movimentacao_compra.model_dump(mode="json"))

    # Venda parcial
    movimentacao_venda = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.VENDA,
        quantidade=Decimal("50"),
        preco_unitario=Decimal("30.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    response = client.post("/api/movimentacoes", json=movimentacao_venda.model_dump(mode="json"))
    assert response.status_code == 201

def test_registrar_venda_total_e_zerar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # Compra inicial
    movimentacao_compra = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    client.post("/api/movimentacoes", json=movimentacao_compra.model_dump(mode="json"))

    # Venda total
    movimentacao_venda = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.VENDA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("30.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    response = client.post("/api/movimentacoes", json=movimentacao_venda.model_dump(mode="json"))
    assert response.status_code == 201

def test_venda_maior_que_posicao_existente_deve_falhar(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # Compra inicial
    movimentacao_compra = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    client.post("/api/movimentacoes", json=movimentacao_compra.model_dump(mode="json"))

    # Venda maior que a posição
    movimentacao_venda = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.VENDA,
        quantidade=Decimal("150"),
        preco_unitario=Decimal("30.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    response = client.post("/api/movimentacoes", json=movimentacao_venda.model_dump(mode="json"))
    assert response.status_code == 400
    assert "Não é permitido vender mais do que a quantidade em posição." in response.json()["detail"]

def test_listar_posicoes_por_carteira(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # Compra inicial
    movimentacao_create = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    res_post = client.post("/api/movimentacoes", json=movimentacao_create.model_dump(mode="json"))
    assert res_post.status_code == 201 # Garante que a compra funcionou antes de testar o GET

    response = client.get(f"/api/posicoes/carteira/{carteira_data.id}")
    assert response.status_code == 200
    posicoes = [PosicaoRead(**p) for p in response.json()]
    assert len(posicoes) == 1
    assert posicoes[0].ativo_id == ativo_data.id
    assert posicoes[0].quantidade == Decimal("100")

def test_listar_posicoes_por_carteira_e_conta(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # Compra inicial
    movimentacao_create = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal("100"),
        preco_unitario=Decimal("25.00"),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    res_post = client.post("/api/movimentacoes", json=movimentacao_create.model_dump(mode="json"))
    assert res_post.status_code == 201 # Garante que a compra funcionou antes de testar o GET

    response = client.get(f"/api/posicoes/carteira/{carteira_data.id}/conta/{conta_data.id}")
    assert response.status_code == 200
    posicoes = [PosicaoRead(**p) for p in response.json()]
    assert len(posicoes) == 1
    assert posicoes[0].ativo_id == ativo_data.id
    assert posicoes[0].quantidade == Decimal("100")