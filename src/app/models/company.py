from sqlalchemy import Column, Integer, String
from src.app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, unique=True, index=True)

    user_links = relationship(
        "UserCompanyRole",
        back_populates="company",
        cascade="all, delete-orphan"
    )
