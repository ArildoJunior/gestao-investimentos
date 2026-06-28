# FILE: backend/migrations/versions/c1a2b3d4e5f6_adiciona_usuario_id_em_contas.py
"""Adiciona usuario_id em contas para isolamento multi-usuário

Revision ID: c1a2b3d4e5f6
Revises: ba8bf0c084a9
Create Date: 2026-06-28
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "c1a2b3d4e5f6"
down_revision = "ba8bf0c084a9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Adiciona a coluna como nullable primeiro (para não quebrar linhas existentes)
    op.add_column(
        "contas",
        sa.Column(
            "usuario_id",
            UUID(as_uuid=True),
            nullable=True,
        ),
    )

    # 2. Preenche registros existentes com o primeiro usuário encontrado
    #    (ambiente de desenvolvimento — em produção use um script específico)
    op.execute(
        """
        UPDATE contas
        SET usuario_id = (SELECT id FROM usuarios ORDER BY created_at LIMIT 1)
        WHERE usuario_id IS NULL
        """
    )

    # 3. Torna a coluna NOT NULL após preencher
    op.alter_column("contas", "usuario_id", nullable=False)

    # 4. Adiciona a FK e o índice
    op.create_foreign_key(
        "fk_contas_usuario_id",
        "contas",
        "usuarios",
        ["usuario_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index("ix_contas_usuario_id", "contas", ["usuario_id"])


def downgrade() -> None:
    op.drop_index("ix_contas_usuario_id", table_name="contas")
    op.drop_constraint("fk_contas_usuario_id", "contas", type_="foreignkey")
    op.drop_column("contas", "usuario_id")