"""add created_at to users

Revision ID: 6f76533047ac
Revises: d36c21687e3c
Create Date: 2026-01-31 09:36:05.774204

"""
from alembic import op
import sqlalchemy as sa


revision = "6f76533047ac"
down_revision = "d36c21687e3c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("users", "created_at")
