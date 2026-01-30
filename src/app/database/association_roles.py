from sqlalchemy import Table, Column, Integer, ForeignKey, String
from src.app.database.base import Base

class UserCompanyRole(Base):
    __tablename__ = "user_company_role"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    company_id = Column(ForeignKey("companies.id"), primary_key=True)
    role = Column(String, nullable=False)

    user = relationship("User", back_populates="company_links")
    company = relationship("Company", back_populates="user_links")
