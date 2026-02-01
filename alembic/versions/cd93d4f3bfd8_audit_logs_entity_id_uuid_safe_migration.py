"""audit_logs entity_id uuid safe migration

Revision ID: cd93d4f3bfd8
Revises: 3d2aaa5c139a
Create Date: 2026-02-01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "cd93d4f3bfd8"
down_revision = "3d2aaa5c139a"
branch_labels = None
depends_on = None


def upgrade():
    # 1. cria nova coluna UUID
    op.add_column(
        "audit_logs",
        sa.Column("entity_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # 2. NÃO converte dados antigos (int -> uuid é inválido)

    # 3. remove coluna antiga
    op.drop_column("audit_logs", "entity_id")

    # 4. renomeia para manter contrato
    op.alter_column(
        "audit_logs",
        "entity_uuid",
        new_column_name="entity_id",
    )


def downgrade():
    op.add_column(
        "audit_logs",
        sa.Column("entity_id", sa.Integer(), nullable=True),
    )
    op.drop_column("audit_logs", "entity_uuid")
