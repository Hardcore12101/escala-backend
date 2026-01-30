"""add paid_at to guides

Revision ID: 3ebb2e7ceab8
Revises: 99aed69ffec9
Create Date: 2026-01-28 09:36:50.913238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ebb2e7ceab8'
down_revision: Union[str, Sequence[str], None] = '99aed69ffec9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
