"""User schemas"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    mobile: str = Field(..., pattern="^[0-9]{10}$")
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict
    http_status: int = 200

class UserResponse(BaseModel):
    id: int
    username: str
    mobile: str
    email: Optional[str]
    status: int
    added_on: datetime
    
    class Config:
        from_attributes = True
