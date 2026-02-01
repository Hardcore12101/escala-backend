from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from datetime import datetime
from src.app.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON




class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)

    entity = Column(String, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
