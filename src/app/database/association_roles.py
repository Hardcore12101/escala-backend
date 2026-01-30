from sqlalchemy import Table, Column, Integer, ForeignKey, String
from src.app.database.base import Base

user_company_role = Table(
    "user_company_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("role", String, nullable=False),
)
