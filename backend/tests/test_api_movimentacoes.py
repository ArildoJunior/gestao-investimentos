# FILE: backend/tests/test_api_movimentacoes.py
from __future__ import annotations

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


def _compra(
    client: TestClient,
    carteira_data: Carteira,
    conta_data: Conta,
    ativo_data: Ativo,
    quantidade: str = "100",
    preco: str = "25.00",
) -> dict:
    """Helper para registrar uma compra e retornar o JSON da resposta."""
    payload = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        quantidade=Decimal(quantidade),
        preco_unitario=Decimal(preco),
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        tipo_operacao=TipoOperacao.SWING,
    )
    res = client.post(
        "/api/movimentacoes",
        json=payload.model_dump(mode="json"),
    )
    assert res.status_code == 201, res.text
    return res.json()


def test_registrar_compra_inicial_e_atualizar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    body = _compra(client, carteira_data, conta_data, ativo_data)
    assert body["quantidade"] == "100.00000000"


def test_registrar_compra_adicional_e_atualizar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    _compra(client, carteira_data, conta_data, ativo_data)
    body = _compra(
        client, carteira_data, conta_data, ativo_data,
        quantidade="50", preco="26.00",
    )
    assert body["quantidade"] == "50.00000000"


def test_registrar_venda_parcial_e_atualizar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    _compra(client, carteira_data, conta_data, ativo_data)

    payload = MovimentacaoCreate(
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
    res = client.post(
        "/api/movimentacoes",
        json=payload.model_dump(mode="json"),
    )
    assert res.status_code == 201, res.text


def test_registrar_venda_total_e_zerar_posicao(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    _compra(client, carteira_data, conta_data, ativo_data)

    payload = MovimentacaoCreate(
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
    res = client.post(
        "/api/movimentacoes",
        json=payload.model_dump(mode="json"),
    )
    assert res.status_code == 201, res.text


def test_venda_maior_que_posicao_existente_deve_falhar(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    _compra(client, carteira_data, conta_data, ativo_data)

    payload = MovimentacaoCreate(
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
    res = client.post(
        "/api/movimentacoes",
        json=payload.model_dump(mode="json"),
    )
    assert res.status_code == 400
    assert "Não é permitido vender mais do que a quantidade em posição." in res.json()["detail"]


def test_listar_posicoes_por_carteira(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    _compra(client, carteira_data, conta_data, ativo_data)

    res = client.get(f"/api/posicoes/carteira/{carteira_data.id}")
    assert res.status_code == 200
    posicoes = [PosicaoRead(**p) for p in res.json()]
    assert len(posicoes) == 1
    assert posicoes[0].ativo_id == ativo_data.id
    assert posicoes[0].quantidade == Decimal("100.00000000")


def test_listar_posicoes_por_carteira_e_conta(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    _compra(client, carteira_data, conta_data, ativo_data)

    res = client.get(
        f"/api/posicoes/carteira/{carteira_data.id}/conta/{conta_data.id}"
    )
    assert res.status_code == 200
    posicoes = [PosicaoRead(**p) for p in res.json()]
    assert len(posicoes) == 1
    assert posicoes[0].quantidade == Decimal("100.00000000")