"""merge heads after users uuid conversion

Revision ID: 9cb0a64cb9de
Revises: 3cab2b657184, 6f76533047ac
Create Date: 2026-01-31 10:05:07.125343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cb0a64cb9de'
down_revision: Union[str, Sequence[str], None] = ('3cab2b657184', '6f76533047ac')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
