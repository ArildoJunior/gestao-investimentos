from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.schemas.enums import TipoProvento


def test_criar_provento_e_listar_por_ativo(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    carteira_data: Carteira,
    conta_data: Conta,
):
    """
    Verifica se:
    - é possível criar um provento via POST /api/proventos
    - ele é retornado pelo GET /api/proventos?ativo_id=...
    """
    payload = {
        "carteira_id": str(carteira_data.id),
        "conta_id": str(conta_data.id),
        "ativo_id": str(ativo_data.id),
        "tipo": TipoProvento.DIVIDENDO.value,
        "valor_bruto": "123.45",
        "data_com": date.today().isoformat(),
        "data_pagamento": date.today().isoformat(),
        "quantidade": "10.00000000",
        "reinvestido": False,
        "observacoes": "Provento de teste",
    }

    # Criação
    res_post = client.post("/api/proventos", json=payload)
    assert res_post.status_code == 201, res_post.text
    body = res_post.json()
    assert body["ativo_id"] == str(ativo_data.id)
    assert body["carteira_id"] == str(carteira_data.id)
    assert Decimal(body["valor_bruto"]) == Decimal("123.45")
    # valor_liquido = valor_bruto nesta fase
    assert Decimal(body["valor_liquido"]) == Decimal("123.45")

    # Listagem por ativo
    res_get = client.get(f"/api/proventos?ativo_id={ativo_data.id}")
    assert res_get.status_code == 200
    itens = res_get.json()
    assert len(itens) >= 1
    # Garante que o provento recém-criado está presente
    ids = [p["id"] for p in itens]
    assert body["id"] in ids


def test_criar_provento_sem_carteira_deve_falhar(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    conta_data: Conta,
):
    """
    Sem carteira_id não pode registrar provento (regra do service).
    """
    payload = {
        "carteira_id": None,
        "conta_id": str(conta_data.id),
        "ativo_id": str(ativo_data.id),
        "tipo": TipoProvento.DIVIDENDO.value,
        "valor_bruto": "50.00",
        "data_com": date.today().isoformat(),
        "data_pagamento": date.today().isoformat(),
        "quantidade": "5.00000000",
        "reinvestido": False,
        "observacoes": "Provento sem carteira",
    }

    res_post = client.post("/api/proventos", json=payload)
    # O service levanta ValueError -> HTTP 400
    assert res_post.status_code == 400
    assert "carteira_id é obrigatório" in res_post.json()["detail"]