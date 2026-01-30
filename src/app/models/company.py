from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.app.database.base import Base
from src.app.database.association_roles import user_company_role

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        secondary=user_company_role,
        back_populates="companies",
    )