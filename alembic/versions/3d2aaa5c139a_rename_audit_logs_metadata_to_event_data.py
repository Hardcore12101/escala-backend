"""rename audit_logs metadata to event_data

Revision ID: 3d2aaa5c139a
Revises: 4490072962f8
Create Date: 2026-02-01
"""

from alembic import op

revision = "3d2aaa5c139a"
down_revision = "4490072962f8"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "audit_logs",
        "metadata",
        new_column_name="event_data",
    )


def downgrade():
    op.alter_column(
        "audit_logs",
        "event_data",
        new_column_name="metadata",
    )
