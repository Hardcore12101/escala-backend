"""company owner refactor

Revision ID: 2767705b3086
Revises: cd93d4f3bfd8
Create Date: 2026-02-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2767705b3086"
down_revision: Union[str, Sequence[str], None] = "cd93d4f3bfd8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Company ownership refactor:
    - Remove user_company_role table
    - Add owner_id to companies
    """

    # Remove legacy many-to-many table
    op.drop_table("user_company_role")

    # Add owner_id as nullable first (safe for existing rows)
    op.add_column(
        "companies",
        sa.Column("owner_id", sa.UUID(), nullable=True),
    )

    # Create FK companies.owner_id -> users.id
    op.create_foreign_key(
        "fk_companies_owner_id_users",
        "companies",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Enforce NOT NULL after column exists
    op.alter_column(
        "companies",
        "owner_id",
        nullable=False,
    )


def downgrade() -> None:
    """
    Revert company ownership refactor
    """

    # Drop FK
    op.drop_constraint(
        "fk_companies_owner_id_users",
        "companies",
        type_="foreignkey",
    )

    # Drop owner_id column
    op.drop_column("companies", "owner_id")

    # Restore legacy table
    op.create_table(
        "user_company_role",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", "company_id"),
    )
