"""promote users.id_uuid to primary key

Revision ID: 651444533c10
Revises: 9cb0a64cb9de
Create Date: 2026-01-31 10:46:22.145584

"""
from alembic import op
import sqlalchemy as sa

revision = "651444533c10"
down_revision = "3cab2b657184"
branch_labels = None
depends_on = None


def upgrade():
    # 1. remover PK antiga
    op.drop_constraint("users_pkey", "users", type_="primary")

    # 2. remover coluna id antiga (int)
    op.drop_column("users", "id")

    # 3. renomear id_uuid → id
    op.alter_column("users", "id_uuid", new_column_name="id")

    # 4. criar nova PK UUID
    op.create_primary_key("users_pkey", "users", ["id"])


def downgrade():
    raise RuntimeError("Downgrade not supported for UUID promotion")
