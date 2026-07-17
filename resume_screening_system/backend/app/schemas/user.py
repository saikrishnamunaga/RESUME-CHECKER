from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    login_type: str
    plan: str = "free"
    daily_usage: int = 0
    monthly_usage: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    plan: str
    daily_usage: int

