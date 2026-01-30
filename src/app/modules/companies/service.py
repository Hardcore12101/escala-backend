from sqlalchemy.orm import Session
from src.app.models.company import Company
from src.app.modules.users.models import User
from src.app.modules.audit.service import log_event


def create_company(
    db: Session,
    name: str,
    cnpj: str,
    user: User
) -> Company:
    company = Company(
        name=name,
        cnpj=cnpj,
    )

    company.users.append(user)

    db.add(company)
    db.commit()
    db.refresh(company)

    log_event(
        db,
        action="CREATE_COMPANY",
        entity="company",
        entity_id=company.id,
    )

    return company
