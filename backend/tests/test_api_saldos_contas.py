from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.enums import TipoSaldoConta


def test_registrar_deposito_em_saldo_conta(
    client: TestClient,
    db_session: Session,
    conta_data: Conta,
):
    saldo_anterior = conta_data.saldo_atual

    payload = {
        "conta_id": str(conta_data.id),
        "tipo": TipoSaldoConta.DEPOSITO.value,
        "valor": "150.25",
        "data_operacao": date.today().isoformat(),
        "descricao": "Depósito teste",
    }

    response = client.post("/api/saldos-contas", json=payload)
    assert response.status_code == 201

    db_session.refresh(conta_data)
    assert conta_data.saldo_atual == saldo_anterior + Decimal("150.25")


def test_registrar_saque_sem_saldo_suficiente_deve_falhar(
    client: TestClient,
    conta_data: Conta,
):
    payload = {
        "conta_id": str(conta_data.id),
        "tipo": TipoSaldoConta.SAQUE.value,
        "valor": "999999999.99",
        "data_operacao": date.today().isoformat(),
        "descricao": "Saque acima do saldo",
    }

    response = client.post("/api/saldos-contas", json=payload)
    assert response.status_code == 400
    assert "Saldo insuficiente" in response.json()["detail"]


def test_listar_saldos_por_conta(
    client: TestClient,
    conta_data: Conta,
):
    payload_1 = {
        "conta_id": str(conta_data.id),
        "tipo": TipoSaldoConta.DEPOSITO.value,
        "valor": "10.00",
        "data_operacao": date.today().isoformat(),
        "descricao": "Depósito 1",
    }
    payload_2 = {
        "conta_id": str(conta_data.id),
        "tipo": TipoSaldoConta.PIX.value,
        "valor": "20.00",
        "data_operacao": date.today().isoformat(),
        "descricao": "PIX 2",
    }

    r1 = client.post("/api/saldos-contas", json=payload_1)
    r2 = client.post("/api/saldos-contas", json=payload_2)
    assert r1.status_code == 201
    assert r2.status_code == 201

    response = client.get(f"/api/saldos-contas?conta_id={conta_data.id}")
    assert response.status_code == 200
    itens = response.json()
    assert len(itens) >= 2