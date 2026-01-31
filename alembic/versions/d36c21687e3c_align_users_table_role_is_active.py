"""align users table (role, is_active)

Revision ID: d36c21687e3c
Revises: ace67cbcc6db
Create Date: 2026-01-31 09:20:29.299153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd36c21687e3c'
down_revision: Union[str, Sequence[str], None] = 'ace67cbcc6db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("role", sa.String(), nullable=False, server_default="user")
    )


def downgrade():
    op.drop_column("users", "role")
