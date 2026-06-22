"""Fase 1 - alinhar schema de movimentacoes e posicoes ao ORM atual

Revision ID: f1_alinhar_mov_pos
Revises: 56ff477d7396
Create Date: 2026-06-22 16:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1_alinhar_mov_pos"
down_revision = "56ff477d7396"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- POSICOES: adiciona custo_total ---
    op.add_column(
        "posicoes",
        sa.Column(
            "custo_total",
            sa.Numeric(precision=20, scale=8),
            nullable=True,
            server_default="0",
        ),
    )
    op.execute("UPDATE posicoes SET custo_total = quantidade * preco_medio WHERE custo_total IS NULL")
    op.alter_column("posicoes", "custo_total", nullable=False)
    op.alter_column("posicoes", "custo_total", server_default=None)

    # --- MOVIMENTACOES: adiciona colunas novas ---
    op.add_column(
        "movimentacoes",
        sa.Column("preco_unitario", sa.Numeric(precision=20, scale=8), nullable=True),
    )
    op.add_column(
        "movimentacoes",
        sa.Column(
            "corretagem",
            sa.Numeric(precision=20, scale=8),
            nullable=True,
            server_default="0",
        ),
    )
    op.add_column(
        "movimentacoes",
        sa.Column(
            "emolumentos",
            sa.Numeric(precision=20, scale=8),
            nullable=True,
            server_default="0",
        ),
    )
    op.add_column(
        "movimentacoes",
        sa.Column(
            "iss",
            sa.Numeric(precision=20, scale=8),
            nullable=True,
            server_default="0",
        ),
    )
    op.add_column(
        "movimentacoes",
        sa.Column(
            "outras_taxas",
            sa.Numeric(precision=20, scale=8),
            nullable=True,
            server_default="0",
        ),
    )
    op.add_column("movimentacoes", sa.Column("data_operacao", sa.Date(), nullable=True))
    op.add_column("movimentacoes", sa.Column("data_liquidacao", sa.Date(), nullable=True))
    op.add_column(
        "movimentacoes",
        sa.Column("valor_bruto", sa.Numeric(precision=20, scale=8), nullable=True),
    )
    op.add_column(
        "movimentacoes",
        sa.Column("valor_liquido", sa.Numeric(precision=20, scale=8), nullable=True),
    )

    # Backfill a partir do schema antigo
    op.execute(
        """
        UPDATE movimentacoes
        SET
            preco_unitario = preco,
            corretagem = custos,
            emolumentos = 0,
            iss = 0,
            outras_taxas = 0,
            data_operacao = data_movimentacao,
            data_liquidacao = data_movimentacao,
            valor_bruto = quantidade * preco,
            valor_liquido = (quantidade * preco) - custos
        """
    )

    # Ajusta not null
    op.alter_column("movimentacoes", "preco_unitario", nullable=False)
    op.alter_column("movimentacoes", "corretagem", nullable=False)
    op.alter_column("movimentacoes", "emolumentos", nullable=False)
    op.alter_column("movimentacoes", "iss", nullable=False)
    op.alter_column("movimentacoes", "outras_taxas", nullable=False)
    op.alter_column("movimentacoes", "data_operacao", nullable=False)
    op.alter_column("movimentacoes", "data_liquidacao", nullable=False)
    op.alter_column("movimentacoes", "valor_bruto", nullable=False)
    op.alter_column("movimentacoes", "valor_liquido", nullable=False)

    # Remove defaults transitórios
    op.alter_column("movimentacoes", "corretagem", server_default=None)
    op.alter_column("movimentacoes", "emolumentos", server_default=None)
    op.alter_column("movimentacoes", "iss", server_default=None)
    op.alter_column("movimentacoes", "outras_taxas", server_default=None)

    # Índice de data_operacao no lugar de data_movimentacao
    op.drop_index("ix_movimentacoes_data_movimentacao", table_name="movimentacoes")
    op.create_index("ix_movimentacoes_data_operacao", "movimentacoes", ["data_operacao"], unique=False)

    # Remove colunas antigas
    op.drop_column("movimentacoes", "preco")
    op.drop_column("movimentacoes", "custos")
    op.drop_column("movimentacoes", "data_movimentacao")


def downgrade() -> None:
    # Recria colunas antigas
    op.add_column(
        "movimentacoes",
        sa.Column("preco", sa.Numeric(precision=20, scale=8), nullable=True),
    )
    op.add_column(
        "movimentacoes",
        sa.Column("custos", sa.Numeric(precision=20, scale=8), nullable=True, server_default="0"),
    )
    op.add_column(
        "movimentacoes",
        sa.Column("data_movimentacao", sa.Date(), nullable=True),
    )

    # Backfill reverso
    op.execute(
        """
        UPDATE movimentacoes
        SET
            preco = preco_unitario,
            custos = COALESCE(corretagem, 0) + COALESCE(emolumentos, 0) + COALESCE(iss, 0) + COALESCE(outras_taxas, 0),
            data_movimentacao = data_operacao
        """
    )

    op.alter_column("movimentacoes", "preco", nullable=False)
    op.alter_column("movimentacoes", "custos", nullable=False)
    op.alter_column("movimentacoes", "data_movimentacao", nullable=False)
    op.alter_column("movimentacoes", "custos", server_default=None)

    op.drop_index("ix_movimentacoes_data_operacao", table_name="movimentacoes")
    op.create_index("ix_movimentacoes_data_movimentacao", "movimentacoes", ["data_movimentacao"], unique=False)

    # Remove colunas novas
    op.drop_column("movimentacoes", "valor_liquido")
    op.drop_column("movimentacoes", "valor_bruto")
    op.drop_column("movimentacoes", "data_liquidacao")
    op.drop_column("movimentacoes", "data_operacao")
    op.drop_column("movimentacoes", "outras_taxas")
    op.drop_column("movimentacoes", "iss")
    op.drop_column("movimentacoes", "emolumentos")
    op.drop_column("movimentacoes", "corretagem")
    op.drop_column("movimentacoes", "preco_unitario")

    # Posicoes
    op.drop_column("posicoes", "custo_total")