from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

# Request: Register
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.USER # Default role is USER

# Request: Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response: Read-only
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_verified: bool
    role: UserRole

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordReset(BaseModel):
    token: str
    new_password: str
