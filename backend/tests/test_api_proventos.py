# FILE: backend/tests/test_api_proventos.py
from datetime import date
from decimal import Decimal
from uuid import UUID
import uuid # Importar o módulo uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.instituicao import Instituicao
from app.schemas.enums import TipoProvento
from app.schemas.provento import ProventoCreate, ProventoRead

def test_criar_provento(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    payload = ProventoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo=TipoProvento.DIVIDENDO,
        valor_bruto=Decimal("10.00"),
        ir_retido=Decimal("1.00"),
        data_com=date(2023, 1, 1),
        data_pagamento=date(2023, 1, 15),
        quantidade_na_data=Decimal("100"),
        reinvestido=False,
        observacoes="Dividendo de PETR4",
    )
    res = client.post(
        "/api/proventos",
        json=payload.model_dump(mode="json"),
    )
    assert res.status_code == 201, res.text
    provento = ProventoRead(**res.json())
    assert provento.valor_bruto == Decimal("10.00")
    assert provento.ir_retido == Decimal("1.00")
    assert provento.valor_liquido == Decimal("9.00")
    assert provento.tipo == TipoProvento.DIVIDENDO
    assert provento.carteira_id == carteira_data.id
    assert provento.ativo_id == ativo_data.id

def test_criar_provento_sem_carteira_deve_falhar(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
):
    # Usar um UUID aleatório que não pertence ao usuário autenticado
    # para testar a validação de posse da carteira.
    random_uuid = uuid.uuid4()
    payload = ProventoCreate(
        carteira_id=random_uuid, # UUID aleatório para forçar erro de posse
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo=TipoProvento.DIVIDENDO,
        valor_bruto=Decimal("10.00"),
        ir_retido=Decimal("0.00"),
        data_com=date(2023, 1, 1),
        data_pagamento=date(2023, 1, 15),
        quantidade_na_data=Decimal("100"),
        reinvestido=False,
        observacoes="Dividendo de PETR4",
    )
    res = client.post(
        "/api/proventos",
        json=payload.model_dump(mode="json"),
    )
    # Esperar 403 Forbidden, pois o service valida a posse da carteira
    assert res.status_code == 403
    assert "Carteira não encontrada ou não pertence ao usuário." in res.json()["detail"]

def test_criar_provento_e_listar_por_ativo(
    client: TestClient,
    db_session: Session,
    instituicao_data: Instituicao,
    conta_data: Conta,
    ativo_data: Ativo,
    carteira_data: Carteira,
):
    payload = ProventoCreate(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        tipo=TipoProvento.JCP,
        valor_bruto=Decimal("5.00"),
        ir_retido=Decimal("0.75"),
        data_com=date(2023, 2, 1),
        data_pagamento=date(2023, 2, 10),
        quantidade_na_data=Decimal("50"),
        reinvestido=False,
        observacoes="JCP de PETR4",
    )
    res_post = client.post(
        "/api/proventos",
        json=payload.model_dump(mode="json"),
    )
    assert res_post.status_code == 201, res_post.text

    res_get = client.get(f"/api/proventos?ativo_id={ativo_data.id}")
    assert res_get.status_code == 200
    proventos = [ProventoRead(**p) for p in res_get.json()]
    assert len(proventos) == 1
    assert proventos[0].ativo_id == ativo_data.id
    assert proventos[0].valor_liquido == Decimal("4.25")

def test_provento_de_outro_usuario_nao_aparece_na_listagem(
    client: TestClient,
    db_session: Session,
    conta_data: Conta,
    carteira_data: Carteira,
):
    """
    Garante que o isolamento por usuario_id funciona no módulo de proventos.
    O GET retorna apenas proventos da carteira do usuário autenticado.
    """
    import uuid

    # Tenta listar proventos de uma carteira que não existe ou não pertence ao usuário
    res_get = client.get(f"/api/proventos?carteira_id={uuid.uuid4()}")
    # Esperar 403 Forbidden, pois o service valida a posse da carteira
    assert res_get.status_code == 403
    assert "Carteira não encontrada ou não pertence ao usuário." in res_get.json()["detail"]
