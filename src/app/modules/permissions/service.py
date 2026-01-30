from sqlalchemy.orm import Session
from app.database.association_roles import user_company_role
from app.modules.permissions.enums import RoleEnum


def assign_role(
    db: Session,
    user_id: int,
    company_id: int,
    role: RoleEnum,
):
    db.execute(
        user_company_role.insert().values(
            user_id=user_id,
            company_id=company_id,
            role=role.value,
        )
    )
    db.commit()
