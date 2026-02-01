"""add user_id to audit_logs

Revision ID: 4490072962f8
Revises: 41f01391a046
Create Date: 2026-02-01 14:20:11.262433
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '4490072962f8'
down_revision: Union[str, Sequence[str], None] = '41f01391a046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'audit_logs',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    op.create_foreign_key(
        'audit_logs_user_id_fkey',
        'audit_logs',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade() -> None:
    op.drop_constraint(
        'audit_logs_user_id_fkey',
        'audit_logs',
        type_='foreignkey'
    )

    op.drop_column('audit_logs', 'user_id')
