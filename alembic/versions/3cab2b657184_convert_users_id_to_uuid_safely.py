"""convert users.id to uuid safely (safe, fk-aware)

Revision ID: 3cab2b657184
Revises: bcb7635615ff
Create Date: 2026-01-31 09:51:42.480759

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3cab2b657184"
down_revision = "bcb7635615ff"
branch_labels = None
depends_on = None


def upgrade():
    # ===============================
    # 1. users: criar nova coluna UUID
    # ===============================
    op.add_column(
        "users",
        sa.Column(
            "id_uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
    )

    # ==========================================
    # 2. user_company_role: nova coluna UUID FK
    # ==========================================
    op.add_column(
        "user_company_role",
        sa.Column(
            "user_id_uuid",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    # ===================================================
    # 3. Remover FK antiga (INTEGER → users.id)
    # ===================================================
    op.drop_constraint(
        "user_company_role_user_id_fkey",
        "user_company_role",
        type_="foreignkey",
    )

    # =====================================
    # 4. Apagar coluna antiga user_id
    # =====================================
    op.drop_column("user_company_role", "user_id")

    # ===================================================
    # 5. Criar nova FK UUID → users.id_uuid
    # ===================================================
    op.create_foreign_key(
        "user_company_role_user_id_fkey",
        "user_company_role",
        "users",
        ["user_id_uuid"],
        ["id_uuid"],
        ondelete="CASCADE",
    )

    # =====================================
    # 6. Apagar PK antiga users.id
    # =====================================
    op.drop_column("users", "id")

    # =====================================
    # 7. Renomear id_uuid → id
    # =====================================
    op.alter_column(
        "users",
        "id_uuid",
        new_column_name="id",
    )

    op.alter_column(
        "user_company_role",
        "user_id_uuid",
        new_column_name="user_id",
    )


def downgrade():
    raise RuntimeError("Downgrade não suportado para conversão de UUID")