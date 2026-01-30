from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

from app.modules.obligations.enums import ObligationType, ObligationStatus


class Obligation(Base):
    __tablename__ = "obligations"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company")

    type = Column(Enum(ObligationType), nullable=False)
    competence = Column(String, nullable=False)  # ex: 2026-01
    due_date = Column(Date, nullable=False)

    status = Column(
        Enum(ObligationStatus),
        default=ObligationStatus.PENDING,
        nullable=False,
    )
