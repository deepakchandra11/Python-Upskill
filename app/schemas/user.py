from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    name: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    name: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

