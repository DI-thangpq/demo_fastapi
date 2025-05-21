from pydantic import BaseModel, Field
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=5000)
    user_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=5000)
    user_id: Optional[int] = None

class Post(PostBase):
    id: int
    class Config:
        from_attributes = True