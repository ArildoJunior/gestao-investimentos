# FILE: backend/tests/test_api_saldos_contas.py
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

    res = client.post("/api/saldos-contas", json=payload)
    assert res.status_code == 201, res.text

    db_session.refresh(conta_data)
    assert conta_data.saldo_atual == saldo_anterior + Decimal("150.25")


def test_registrar_saque_sem_saldo_suficiente_deve_falhar(
    client: TestClient,
    db_session: Session,
    conta_data: Conta,
):
    payload = {
        "conta_id": str(conta_data.id),
        "tipo": TipoSaldoConta.SAQUE.value,
        "valor": "999999999.99",
        "data_operacao": date.today().isoformat(),
        "descricao": "Saque acima do saldo",
    }

    res = client.post("/api/saldos-contas", json=payload)
    assert res.status_code == 400
    assert "Saldo insuficiente" in res.json()["detail"]


def test_listar_saldos_por_conta(
    client: TestClient,
    db_session: Session,
    conta_data: Conta,
):
    for tipo, valor, desc in [
        (TipoSaldoConta.DEPOSITO, "10.00", "Depósito 1"),
        (TipoSaldoConta.PIX, "20.00", "PIX 2"),
    ]:
        res = client.post(
            "/api/saldos-contas",
            json={
                "conta_id": str(conta_data.id),
                "tipo": tipo.value,
                "valor": valor,
                "data_operacao": date.today().isoformat(),
                "descricao": desc,
            },
        )
        assert res.status_code == 201, res.text

    res_get = client.get(f"/api/saldos-contas?conta_id={conta_data.id}")
    assert res_get.status_code == 200
    assert len(res_get.json()) >= 2


def test_saldo_conta_nao_pertence_ao_usuario_deve_retornar_403(
    client: TestClient,
    db_session: Session,
):
    """
    UUID aleatório que não existe no banco deve retornar 403,
    nunca 500 — garante que o isolamento por usuário está funcionando.
    """
    import uuid

    payload = {
        "conta_id": str(uuid.uuid4()),
        "tipo": TipoSaldoConta.DEPOSITO.value,
        "valor": "100.00",
        "data_operacao": date.today().isoformat(),
        "descricao": "Conta de outro usuário",
    }

    res = client.post("/api/saldos-contas", json=payload)
    assert res.status_code == 403