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
    conn = op.get_bind()

    # remove PK atual (qualquer nome)
    conn.execute(sa.text("""
        DO $$
        DECLARE
            constraint_name text;
        BEGIN
            SELECT conname INTO constraint_name
            FROM pg_constraint
            WHERE conrelid = 'users'::regclass
              AND contype = 'p';

            IF constraint_name IS NOT NULL THEN
                EXECUTE format('ALTER TABLE users DROP CONSTRAINT %I', constraint_name);
            END IF;
        END$$;
    """))

    # recria PK corretamente
    op.create_primary_key("users_pkey", "users", ["id"])


def downgrade():
    raise RuntimeError("Downgrade not supported for UUID promotion")
