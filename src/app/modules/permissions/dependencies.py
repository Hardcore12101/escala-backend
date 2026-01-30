from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.database.association_roles import user_company_role
from app.modules.permissions.enums import RoleEnum
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User


def require_role(role: RoleEnum):
    def checker(
        company_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        result = db.execute(
            user_company_role.select().where(
                (user_company_role.c.user_id == user.id) &
                (user_company_role.c.company_id == company_id) &
                (user_company_role.c.role == role.value)
            )
        ).first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente",
            )

        return True

    return checker
