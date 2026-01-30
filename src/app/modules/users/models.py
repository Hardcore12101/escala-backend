from sqlalchemy import Column, Integer, String, Boolean
from src.app.database.base import Base
from src.app.database.association_roles import user_company_role
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    companies = relationship(
        "Company",
        secondary=user_company_role,
        back_populates="users",
    )