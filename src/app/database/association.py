from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

user_company = Table(
    "user_company",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
)
