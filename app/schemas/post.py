from pydantic import BaseModel, Field
from typing import Optional
from app.models.user import User  # Import User thay vì Post

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
    # user: Optional[User] = None  # Tùy chọn, có thể bỏ nếu không cần trả về user

    class Config:
        from_attributes = True