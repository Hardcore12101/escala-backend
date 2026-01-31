from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    role: str | None = None
    is_active: bool | None = None
    
class AddUserToCompanySchema(BaseModel):
    user_id: UUID
    role: str