from sqlalchemy import Table, Column, Integer, ForeignKey, String
from src.app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

user_company_role = Table(
    "user_company_role",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("role", String(50), nullable=False),
)
