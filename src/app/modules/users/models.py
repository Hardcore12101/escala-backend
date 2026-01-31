from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from src.app.database.base import Base
from src.app.database.association_roles import user_company_role
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID
from src.app.models.company import Company

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False, default="user")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    companies = relationship(
        "Company",
        secondary=user_company_role,
        back_populates="users",
    )

class UserCompany(Base):
    __tablename__ = "user_companies"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    role = Column(String, nullable=False, default="member")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
