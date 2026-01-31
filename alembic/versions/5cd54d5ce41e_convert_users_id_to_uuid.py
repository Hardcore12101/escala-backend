"""convert users.id to uuid

Revision ID: 5cd54d5ce41e
Revises: 6f76533047ac
Create Date: 2026-01-31 09:45:29.323045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "5cd54d5ce41e"
down_revision = "6f76533047ac"
branch_labels = None
depends_on = None


def upgrade():
    # cria coluna nova temporária
    op.add_column(
        "users",
        sa.Column("id_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # preenche com uuid novo
    op.execute("UPDATE users SET id_uuid = gen_random_uuid()")

    # remove FKs dependentes se existirem (por enquanto não há)
    op.drop_column("users", "id")
    op.alter_column("users", "id_uuid", new_column_name="id", nullable=False)
    op.create_primary_key("pk_users", "users", ["id"])


def downgrade():
    raise NotImplementedError("Downgrade not supported")
