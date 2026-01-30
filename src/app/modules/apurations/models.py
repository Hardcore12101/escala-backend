from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from src.app.database.base import Base



class Apuration(Base):
    __tablename__ = "apurations"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    competence = Column(String, nullable=False)  # ex: 2026-01

    total_base = Column(Numeric(14, 2), nullable=False)
    total_tax = Column(Numeric(14, 2), nullable=False)

    status = Column(String, default="CLOSED")

    company = relationship("Company")
