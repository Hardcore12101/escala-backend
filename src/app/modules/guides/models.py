from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy.sql import func

from app.database.base import Base



class Guide(Base):
    __tablename__ = "guides"

    id = Column(Integer, primary_key=True)
    apuration_id = Column(Integer, ForeignKey("apurations.id"), nullable=False)
    guide_type = Column(String, nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="PENDING")
    paid_at = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
