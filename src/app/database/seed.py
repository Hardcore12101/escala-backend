from sqlalchemy.orm import Session

from src.app.models.company import Company
from src.app.modules.users.models import User
from src.app.database.association_roles import user_company_role
from src.app.modules.permissions.enums import RoleEnum


def seed_system_company(db: Session):
    # Verifica se já existe
    company = db.query(Company).filter(Company.name == "Escala Digital").first()
    if company:
        return company

    company = Company(
        name="Escala Digital",
        cnpj="00000000000000"
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company
