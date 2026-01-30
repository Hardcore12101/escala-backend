from sqlalchemy import Column, Integer, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.app.database.base import Base



class TaxCalculation(Base):
    __tablename__ = "tax_calculations"

    id = Column(Integer, primary_key=True, index=True)

    obligation_id = Column(Integer, ForeignKey("obligations.id"), nullable=False)
    tax_rule_id = Column(Integer, ForeignKey("tax_rules.id"), nullable=False)

    base_amount = Column(Numeric(14, 2), nullable=False)
    percentage = Column(Numeric(5, 2), nullable=False)
    tax_amount = Column(Numeric(14, 2), nullable=False)

    calculated_at = Column(Date, nullable=False)

    obligation = relationship("Obligation")
