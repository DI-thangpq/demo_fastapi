from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.models.user import User

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    return result.scalars().first()

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Post).offset(skip).limit(limit))
    return result.scalars().all()

async def create_post(db: AsyncSession, post: PostCreate, current_user_id: int):
    result = await db.execute(select(User).filter(User.id == post.user_id))
    if not result.scalars().first():
        raise ValueError("User ID does not exist")
    if post.user_id != current_user_id:
        raise ValueError("You can only create posts for yourself")
    db_post = Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def update_post(db: AsyncSession, post_id: int, post: PostUpdate, current_user_id: int):
    db_post = await get_post(db, post_id)
    if db_post:
        if db_post.user_id != current_user_id:
            raise ValueError("You can only update your own posts")
        for key, value in post.dict(exclude_unset=True).items():
            setattr(db_post, key, value)
        await db.commit()
        await db.refresh(db_post)
    return db_post