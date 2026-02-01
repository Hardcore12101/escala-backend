"""rename audit_logs metadata to event_data

Revision ID: 3d2aaa5c139a
Revises: 01ce36d45a0a
Create Date: 2026-02-01 12:14:26.133873

"""
from alembic import op


revision = "3d2aaa5c139a"
down_revision = "01ce36d45a0a"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "audit_logs",
        "metadata",
        new_column_name="event_data"
    )


def downgrade():
    op.alter_column(
        "audit_logs",
        "event_data",
        new_column_name="metadata"
    )
