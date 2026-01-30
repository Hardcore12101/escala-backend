from sqlalchemy import Column, Integer, String, Boolean


from src.app.database.base import Base
from src.app.database.association_roles import user_company_role


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

