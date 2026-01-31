"""add user_company relation

Revision ID: 41f01391a046
Revises: a4e9973b7085
Create Date: 2026-01-31 15:25:29.242257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41f01391a046'
down_revision: Union[str, Sequence[str], None] = 'a4e9973b7085'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
