"""change audit_logs entity_id to uuid

Revision ID: 01ce36d45a0a
Revises: 4490072962f8
Create Date: 2026-02-01 12:07:37.396109

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "01ce36d45a0a"
down_revision = "4490072962f8"
branch_labels = None
depends_on = None


def upgrade():
    # segurança: limpa entity_id antigo incompatível
    op.execute("UPDATE audit_logs SET entity_id = NULL")

    op.alter_column(
        "audit_logs",
        "entity_id",
        type_=postgresql.UUID(as_uuid=True),
        nullable=True,
        postgresql_using="entity_id::uuid"
    )


def downgrade():
    op.alter_column(
        "audit_logs",
        "entity_id",
        type_=sa.Integer(),
        nullable=True,
        postgresql_using="entity_id::integer"
    )
