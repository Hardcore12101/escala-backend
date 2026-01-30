from sqlalchemy import Column, Integer, String, Numeric, Date
from src.app.database.base import Base



class TaxRule(Base):
    __tablename__ = "tax_rules"

    id = Column(Integer, primary_key=True, index=True)

    tax_type = Column(String, nullable=False)  # ex: DAS, IRPJ
    percentage = Column(Numeric(5, 2), nullable=False)  # ex: 27.00

    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=True)  # null = vigente
