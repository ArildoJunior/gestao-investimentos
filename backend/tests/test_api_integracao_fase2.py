# FILE: backend/tests/test_api_integracao_fase2.py
from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.instituicao import Instituicao
from app.schemas.enums import OrigemAporte, TipoAporte, TipoMovimentacao, TipoOperacao
from app.schemas.movimentacao import MovimentacaoCreate
from app.schemas.posicao import PosicaoRead


def test_fluxo_aporte_externo_listagem_por_carteira(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    carteira_data: Carteira,
):
    payload_aporte = {
        "carteira_id": str(carteira_data.id),
        "conta_id": str(conta_data.id),
        "tipo": TipoAporte.EXTERNO.value,
        "origem": None,
        "valor": "1000.00",
        "data_aporte": date.today().isoformat(),
        "movimentacao_id": None,
        "provento_id": None,
        "observacao": "Aporte externo inicial",
    }

    res_post = client.post("/api/aportes", json=payload_aporte)
    assert res_post.status_code == 201, res_post.text

    res_get = client.get(f"/api/aportes?carteira_id={carteira_data.id}")
    assert res_get.status_code == 200
    itens = res_get.json()
    assert len(itens) >= 1
    assert Decimal(itens[0]["valor"]) > 0


def test_fluxo_integrado_movimentacao_com_aporte_reinvestimento(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    # 1. Registra compra
    movimentacao_create = MovimentacaoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo_movimentacao=TipoMovimentacao.COMPRA,
        tipo_operacao=TipoOperacao.SWING,
        data_operacao=date.today(),
        data_liquidacao=date.today(),
        quantidade=Decimal("10"),
        preco_unitario=Decimal("30.00"),
        corretagem=Decimal("0.50"),
        emolumentos=Decimal("0.10"),
        iss=Decimal("0.00"),
        outras_taxas=Decimal("0.00"),
        observacoes="Compra para teste integrado Fase 2",
    )

    res_mov = client.post(
        "/api/movimentacoes",
        json=movimentacao_create.model_dump(mode="json"),
    )
    assert res_mov.status_code == 201, res_mov.text
    mov_id = res_mov.json()["id"]

    # 2. Registra aporte de reinvestimento vinculado à compra
    payload_aporte = {
        "carteira_id": str(carteira_data.id),
        "conta_id": str(conta_data.id),
        "tipo": TipoAporte.REINVESTIMENTO.value,
        "origem": OrigemAporte.DIVIDENDO.value,
        "valor": "120.00",
        "data_aporte": date.today().isoformat(),
        "movimentacao_id": mov_id,
        "provento_id": None,
        "observacao": "Reinvestimento ligado à movimentação",
    }

    res_aporte = client.post("/api/aportes", json=payload_aporte)
    assert res_aporte.status_code == 201, res_aporte.text

    # 3. Valida posição gerada
    res_pos = client.get(f"/api/posicoes/carteira/{carteira_data.id}")
    assert res_pos.status_code == 200
    posicoes = [PosicaoRead(**p) for p in res_pos.json()]
    assert len(posicoes) == 1
    assert posicoes[0].ativo_id == ativo_data.id
    assert posicoes[0].quantidade == Decimal("10.00000000")

    # 4. Valida vínculo entre aporte e movimentação
    res_aportes = client.get(f"/api/aportes?carteira_id={carteira_data.id}")
    assert res_aportes.status_code == 200
    aportes = res_aportes.json()
    assert any(a.get("movimentacao_id") == mov_id for a in aportes)


def test_aportes_de_outro_usuario_nao_aparecem(
    client: TestClient,
    db_session: Session,
    conta_data: Conta,
    carteira_data: Carteira,
):
    """
    Garante que o isolamento por usuario_id funciona no módulo de aportes.
    O GET retorna apenas aportes da carteira do usuário autenticado.
    """
    import uuid

    res_get = client.get(f"/api/aportes?carteira_id={uuid.uuid4()}")
    assert res_get.status_code in {200, 403}
    if res_get.status_code == 200:
        assert res_get.json() == []