# FILE: backend/tests/conftest.py

import os
import sys
from pathlib import Path
from decimal import Decimal
from datetime import date

# Adiciona o diretório 'backend' ao sys.path para resolver importações
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Importa a Base do seu módulo de modelos, não do app.database
from app.models.base import Base
from app.database import get_db
from app.models.usuario import Usuario
from app.models.instituicao import Instituicao
from app.models.conta import Conta
from app.models.carteira import Carteira
from app.models.ativo import Ativo
from app.models.posicao import Posicao
from app.models.movimentacao import Movimentacao

# Importa todos os enums necessários do arquivo centralizado
from app.schemas.enums import (
    TipoInstituicao, StatusInstituicao,
    TipoConta, StatusConta, Moeda,
    TipoAtivo, StatusAtivo, RegiaoAtivo, SegmentoFII,
    TipoCarteira, ObjetivoCarteira,
    TipoMovimentacao, TipoOperacao,
    TipoProvento,
    TipoRendaFixa, IndexadorRendaFixa, LiquidezRendaFixa, StatusRendaFixa,
    StatusAluguel,
    TipoEventoCorporativo,
    TipoApuracaoIR, StatusDARF,
    TipoAlerta,
    TipoMeta,
    TipoRelatorio,
    TipoEntidadeAuditoria, AcaoAuditoria,
    TipoOpcao, EstiloOpcao, DirecaoOpcao, StatusOpcao
)

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados de teste
@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine) # Limpa o banco após os testes

# Sobrescreve a dependência get_db para usar o banco de dados de teste
@pytest.fixture(name="client")
def client_fixture(db_session: Session):
    from main import app as fastapi_app

    def override_get_db():
        yield db_session
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()

# --- Fixtures de Dados de Teste ---

@pytest.fixture
def usuario_data(db_session: Session) -> Usuario:
    usuario = Usuario(
        nome="Usuario Teste",
        email="teste@teste.com",
        senha_hash="hash_falso"
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario

@pytest.fixture
def instituicao_data(db_session: Session) -> Instituicao:
    instituicao = Instituicao(
        nome="Corretora Teste",
        tipo=TipoInstituicao.CORRETORA,
        status=StatusInstituicao.ATIVA,
    )
    db_session.add(instituicao)
    db_session.commit()
    db_session.refresh(instituicao)
    return instituicao

@pytest.fixture
def conta_data(db_session: Session, instituicao_data: Instituicao) -> Conta:
    conta = Conta(
        instituicao_id=instituicao_data.id,
        nome="Conta Corrente Teste",
        tipo=TipoConta.CORRENTE,
        moeda=Moeda.BRL,
        saldo_atual=Decimal("10000.00"),
        saldo_inicial=Decimal("10000.00"),
        data_abertura=date.today(),
        status=StatusConta.ATIVA,
    )
    db_session.add(conta)
    db_session.commit()
    db_session.refresh(conta)
    return conta

@pytest.fixture
def carteira_data(db_session: Session, usuario_data: Usuario) -> Carteira:
    carteira = Carteira(
        usuario_id=usuario_data.id,
        nome="Minha Carteira Teste",
        tipo=TipoCarteira.REAL,
        objetivo=ObjetivoCarteira.CRESCIMENTO,
        descricao="Carteira para testes de crescimento",
        ativa=True,
        saldo_inicial=Decimal("0.00"),
        saldo_atual=Decimal("0.00"),
    )
    db_session.add(carteira)
    db_session.commit()
    db_session.refresh(carteira)
    return carteira

@pytest.fixture
def ativo_data(db_session: Session) -> Ativo:
    ativo = Ativo(
        ticker="PETR4",
        nome="Petrobras PN",
        classe=TipoAtivo.ACAO,
        setor="Petróleo e Gás",
        pais="BR",
        regiao=RegiaoAtivo.BRASIL,
        moeda=Moeda.BRL,
        status=StatusAtivo.ATIVO,
    )
    db_session.add(ativo)
    db_session.commit()
    db_session.refresh(ativo)
    return ativo

@pytest.fixture
def posicao_data(db_session: Session, carteira_data: Carteira, conta_data: Conta, ativo_data: Ativo) -> Posicao:
    posicao = Posicao(
        carteira_id=carteira_data.id,
        conta_id=conta_data.id,
        ativo_id=ativo_data.id,
        quantidade=Decimal("100"),
        preco_medio=Decimal("25.00"),
        custo_total=Decimal("2500.00"),
    )
    db_session.add(posicao)
    db_session.commit()
    db_session.refresh(posicao)
    return posicao

@pytest.fixture
def movimentacao_compra_data(carteira_data: Carteira, conta_data: Conta, ativo_data: Ativo) -> dict:
    return {
        "carteira_id": str(carteira_data.id),
        "conta_id": str(conta_data.id),
        "ativo_id": str(ativo_data.id),
        "tipo_movimentacao": TipoMovimentacao.COMPRA.value,
        "tipo_operacao": TipoOperacao.SWING.value,
        "data_operacao": date(2023, 1, 1).isoformat(),
        "data_liquidacao": date(2023, 1, 3).isoformat(),
        "quantidade": 10,
        "preco_unitario": 30.00,
        "corretagem": 0.50,
        "emolumentos": 0.02,
        "iss": 0.01,
        "outras_taxas": 0.05,
        "observacoes": "Compra inicial de PETR4",
    }

@pytest.fixture
def movimentacao_venda_data(carteira_data: Carteira, conta_data: Conta, ativo_data: Ativo) -> dict:
    return {
        "carteira_id": str(carteira_data.id),
        "conta_id": str(conta_data.id),
        "ativo_id": str(ativo_data.id),
        "tipo_movimentacao": TipoMovimentacao.VENDA.value,
        "tipo_operacao": TipoOperacao.SWING.value,
        "data_operacao": date(2023, 2, 1).isoformat(),
        "data_liquidacao": date(2023, 2, 3).isoformat(),
        "quantidade": 5,
        "preco_unitario": 32.00,
        "corretagem": 0.50,
        "emolumentos": 0.02,
        "iss": 0.01,
        "outras_taxas": 0.05,
        "observacoes": "Venda parcial de PETR4",
    }