
from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    content: str | None = None
    post_id: int | None = None
    user_id: int | None = None
    
class Comment(CommentBase):
    id: int

    class Config:
        from_attributes = True