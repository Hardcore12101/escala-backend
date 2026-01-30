from sqlalchemy import Table, Column, Integer, ForeignKey, String
from src.app.database.base import Base
from sqlalchemy.orm import relationship

user_company_role = Table(
    "user_company_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("role", String, nullable=False),
)

