"""merge heads

Revision ID: a4e9973b7085
Revises: 651444533c10, 9cb0a64cb9de
Create Date: 2026-01-31 10:58:08.628255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4e9973b7085'
down_revision: Union[str, Sequence[str], None] = ('651444533c10', '9cb0a64cb9de')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass

def downgrade():
    pass