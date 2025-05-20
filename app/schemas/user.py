from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from app.models.user import Role

class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[Role] = Role.USER
    
class UserCreate(UserBase):
    password: str = Body(..., min_length=1, max_length=20)

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None