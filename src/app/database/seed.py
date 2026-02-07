from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.app.models.company import Company
from src.app.modules.users.models import User
from src.app.modules.permissions.enums import RoleEnum
from src.app.core.security import get_password_hash


def seed_system_company(db: Session):
    try:
        # COMPANY
        company = db.query(Company).filter(
            Company.name == "Escala Digital"
        ).first()

        if not company:
            company = Company(
                name="Escala Digital",
                cnpj="00000000000000"
            )
            db.add(company)
            db.flush()  # 👈 NÃO commit ainda

        # USER ADMIN
        admin = db.query(User).filter(
            User.email == "admin@escaladigital.com"
        ).first()

        if not admin:
            admin = User(
                email="admin@escaladigital.com",
                hashed_password=get_password_hash("Admin@123"),
                is_active=True,
            )
            db.add(admin)
            db.flush()

        # ROLE (idempotente)
        exists = db.execute(
            user_company_role.select().where(
                (user_company_role.c.user_id == admin.id) &
                (user_company_role.c.company_id == company.id)
            )
        ).first()

        if not exists:
            db.execute(
                user_company_role.insert().values(
                    user_id=admin.id,
                    company_id=company.id,
                    role=RoleEnum.admin.value,
                )
            )

        db.commit()  # 👈 UM commit só, no final

    except SQLAlchemyError as e:
        db.rollback()  # 👈 ISSO EVITA STARTUP TRAVADO
        raise e
