from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.models.saldo_conta import SaldoConta
from app.schemas.enums import TipoSaldoConta
from app.schemas.saldo_conta import SaldoContaCreate


def _calcular_delta_saldo(tipo: TipoSaldoConta, valor: Decimal) -> Decimal:
    if tipo in {TipoSaldoConta.DEPOSITO, TipoSaldoConta.PIX, TipoSaldoConta.TED, TipoSaldoConta.AJUSTE}:
        return valor
    if tipo in {TipoSaldoConta.SAQUE, TipoSaldoConta.TRANSFERENCIA}:
        return -valor
    raise ValueError("Tipo de saldo_conta inválido.")


def registrar_saldo_conta(db: Session, payload: SaldoContaCreate) -> SaldoConta:
    try:
        conta = db.get(Conta, payload.conta_id)
        if conta is None:
            raise ValueError("Conta não encontrada.")

        delta = _calcular_delta_saldo(payload.tipo, payload.valor)
        novo_saldo = (conta.saldo_atual or Decimal("0")) + delta

        if novo_saldo < Decimal("0"):
            raise ValueError("Saldo insuficiente para realizar esta operação.")

        registro = SaldoConta(
            conta_id=payload.conta_id,
            tipo=payload.tipo,
            valor=payload.valor,
            data_operacao=payload.data_operacao,
            descricao=payload.descricao,
        )

        conta.saldo_atual = novo_saldo

        db.add(registro)
        db.commit()
        db.refresh(registro)
        return registro
    except ValueError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise RuntimeError("Erro interno ao registrar saldo de conta.") from exc


def listar_saldos_conta(db: Session, conta_id: UUID) -> list[SaldoConta]:
    return (
        db.query(SaldoConta)
        .filter(SaldoConta.conta_id == conta_id)
        .order_by(SaldoConta.data_operacao.desc(), SaldoConta.created_at.desc())
        .all()
    )


def get_saldo_conta_by_id(db: Session, saldo_conta_id: UUID) -> SaldoConta | None:
    return db.get(SaldoConta, saldo_conta_id)