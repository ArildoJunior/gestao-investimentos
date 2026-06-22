from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.ativo import Ativo
from app.models.carteira import Carteira
from app.models.conta import Conta
from app.models.posicao import Posicao
from app.schemas.enums import TipoEventoCorporativo
from app.schemas.evento_corporativo import EventoCorporativoCreate


def _criar_posicao_inicial(
    db_session: Session,
    carteira: Carteira,
    conta: Conta,
    ativo: Ativo,
    quantidade: Decimal,
    preco_medio: Decimal,
) -> Posicao:
    pos = Posicao(
        carteira_id=carteira.id,
        conta_id=conta.id,
        ativo_id=ativo.id,
        quantidade=quantidade,
        preco_medio=preco_medio,
        custo_total=quantidade * preco_medio,
    )
    db_session.add(pos)
    db_session.commit()
    db_session.refresh(pos)
    return pos


def test_split_aumenta_quantidade_e_ajusta_pm(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    carteira_data: Carteira,
    conta_data: Conta,
):
    """
    SPLIT: quantidade *= fator; pm /= fator; custo_total preservado.
    Ex.: 100 a 20, fator 2 => 200 a 10.
    """
    pos = _criar_posicao_inicial(
        db_session,
        carteira_data,
        conta_data,
        ativo_data,
        quantidade=Decimal("100"),
        preco_medio=Decimal("20"),
    )

    payload = EventoCorporativoCreate(
        ativo_id=ativo_data.id,
        tipo=TipoEventoCorporativo.SPLIT,
        data_evento=date.today(),
        fator=Decimal("2"),
        valor=None,
        ativo_destino_id=None,
        observacoes="Split 1:2",
    )

    res_evento = client.post("/api/eventos-corporativos", json=payload.model_dump(mode="json"))
    assert res_evento.status_code == 201
    evento_id = res_evento.json()["id"]

    res_proc = client.post(f"/api/eventos-corporativos/{evento_id}/processar")
    assert res_proc.status_code == 200

    db_session.refresh(pos)
    assert pos.quantidade == Decimal("200.00000000")
    assert pos.preco_medio == Decimal("10.00000000")
    assert pos.custo_total == Decimal("2000.00000000")


def test_grupamento_reduz_quantidade_e_aumenta_pm(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    carteira_data: Carteira,
    conta_data: Conta,
):
    """
    GRUPAMENTO: quantidade /= fator; pm *= fator; custo_total preservado.
    Ex.: 100 a 5, fator 10 => 10 a 50.
    """
    pos = _criar_posicao_inicial(
        db_session,
        carteira_data,
        conta_data,
        ativo_data,
        quantidade=Decimal("100"),
        preco_medio=Decimal("5"),
    )

    payload = EventoCorporativoCreate(
        ativo_id=ativo_data.id,
        tipo=TipoEventoCorporativo.GRUPAMENTO,
        data_evento=date.today(),
        fator=Decimal("10"),
        valor=None,
        ativo_destino_id=None,
        observacoes="Grupamento 10:1",
    )

    res_evento = client.post("/api/eventos-corporativos", json=payload.model_dump(mode="json"))
    assert res_evento.status_code == 201
    evento_id = res_evento.json()["id"]

    res_proc = client.post(f"/api/eventos-corporativos/{evento_id}/processar")
    assert res_proc.status_code == 200

    db_session.refresh(pos)
    assert pos.quantidade == Decimal("10.00000000")
    assert pos.preco_medio == Decimal("50.00000000")
    assert pos.custo_total == Decimal("500.00000000")


def test_bonificacao_aumenta_quantidade_mantendo_custo_quando_valor_zero(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    carteira_data: Carteira,
    conta_data: Conta,
):
    """
    BONIFICACAO com valor None → custo das novas cotas = 0.
    Ex.: 100 a 20 (custo 2000), fator 1.10 → +10 cotas a custo zero.
    Nova quantidade: 110, custo 2000, pm ≈ 18.18181818.
    """
    pos = _criar_posicao_inicial(
        db_session,
        carteira_data,
        conta_data,
        ativo_data,
        quantidade=Decimal("100"),
        preco_medio=Decimal("20"),
    )

    payload = EventoCorporativoCreate(
        ativo_id=ativo_data.id,
        tipo=TipoEventoCorporativo.BONIFICACAO,
        data_evento=date.today(),
        fator=Decimal("1.10"),  # bonificação de 10%
        valor=None,  # custo zero por cota bonificada
        ativo_destino_id=None,
        observacoes="Bonificação 10%",
    )

    res_evento = client.post("/api/eventos-corporativos", json=payload.model_dump(mode="json"))
    assert res_evento.status_code == 201
    evento_id = res_evento.json()["id"]

    res_proc = client.post(f"/api/eventos-corporativos/{evento_id}/processar")
    assert res_proc.status_code == 200

    db_session.refresh(pos)
    assert pos.quantidade == Decimal("110.00000000")
    # custo total deve continuar 2000
    assert pos.custo_total == Decimal("2000.00000000")
    # PM aproximado 18.18181818 (com arredondamento a 8 casas)
    assert pos.preco_medio == Decimal("18.18181818")


def test_subscricao_trata_como_compra_a_preco_especifico(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    carteira_data: Carteira,
    conta_data: Conta,
):
    """
    SUBSCRICAO: interpreta fator como percentual da posição.
    Ex.: 100 a 20, fator 0.5, preco subscrição 15 → compra 50 cotas a 15.
    """
    pos = _criar_posicao_inicial(
        db_session,
        carteira_data,
        conta_data,
        ativo_data,
        quantidade=Decimal("100"),
        preco_medio=Decimal("20"),
    )

    payload = EventoCorporativoCreate(
        ativo_id=ativo_data.id,
        tipo=TipoEventoCorporativo.SUBSCRICAO,
        data_evento=date.today(),
        fator=Decimal("0.5"),  # direito a 50% da posição
        valor=Decimal("15.00"),  # preço de subscrição por cota
        ativo_destino_id=None,
        observacoes="Subscrição 50% a 15",
    )

    res_evento = client.post("/api/eventos-corporativos", json=payload.model_dump(mode="json"))
    assert res_evento.status_code == 201
    evento_id = res_evento.json()["id"]

    res_proc = client.post(f"/api/eventos-corporativos/{evento_id}/processar")
    assert res_proc.status_code == 200

    db_session.refresh(pos)
    # quantidade: 100 + 50 = 150
    assert pos.quantidade == Decimal("150.00000000")
    # custo anterior = 100*20 = 2000, custo novo = 50*15 = 750 => total 2750
    # pm = 2750 / 150 = 18.33333333
    assert pos.preco_medio == Decimal("18.33333333")
    assert pos.custo_total == Decimal("2750.00000000")


def test_amortizacao_reduz_pm(
    client: TestClient,
    db_session: Session,
    ativo_data: Ativo,
    carteira_data: Carteira,
    conta_data: Conta,
):
    """
    AMORTIZACAO: reduz o PM por cota; custo_total ajustado.
    Ex.: 100 a 20, amortização 5 => novo PM 15.
    """
    pos = _criar_posicao_inicial(
        db_session,
        carteira_data,
        conta_data,
        ativo_data,
        quantidade=Decimal("100"),
        preco_medio=Decimal("20"),
    )

    payload = EventoCorporativoCreate(
        ativo_id=ativo_data.id,
        tipo=TipoEventoCorporativo.AMORTIZACAO,
        data_evento=date.today(),
        fator=Decimal("1"),  # fator não altera quantidade
        valor=Decimal("5.00"),  # valor amortizado por cota
        ativo_destino_id=None,
        observacoes="Amortização 5 por cota",
    )

    res_evento = client.post("/api/eventos-corporativos", json=payload.model_dump(mode="json"))
    assert res_evento.status_code == 201
    evento_id = res_evento.json()["id"]

    res_proc = client.post(f"/api/eventos-corporativos/{evento_id}/processar")
    assert res_proc.status_code == 200

    db_session.refresh(pos)
    assert pos.quantidade == Decimal("100.00000000")
    assert pos.preco_medio == Decimal("15.00000000")
    assert pos.custo_total == Decimal("1500.00000000")