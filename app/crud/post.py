from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.models.user import User

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate, current_user_id: int):
    # Kiểm tra user_id có tồn tại
    if not db.query(User).filter(User.id == post.user_id).first():
        raise ValueError("User ID does not exist")
    # Đảm bảo post thuộc về user hiện tại hoặc admin
    if post.user_id != current_user_id:
        raise ValueError("You can only create posts for yourself")
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: PostUpdate, current_user_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        if db_post.user_id != current_user_id:
            raise ValueError("You can only update your own posts")
        for key, value in post.dict(exclude_unset=True).items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post