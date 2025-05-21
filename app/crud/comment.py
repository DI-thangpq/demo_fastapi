from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate, CommentPatch

async def create_comment(db:AsyncSession, comment: CommentCreate, current_user_id: int):
    result = await db.execute(select(Post).filter(Post.id == comment.post_id))
    if not result.scalars().first():
        raise ValueError("Post ID does not exist")
    if comment.user_id != current_user_id:
        raise ValueError("You can only create comments for yourself")
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_comments(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Comment).offset(skip).limit(limit))
    return result.scalars().all()

async def get_comment(db: AsyncSession, comment_id: int):
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    return result.scalars().first()

async def update_comment(db: AsyncSession, comment_id: int, comment: CommentPatch, current_user_id: int):
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        if db_comment.user_id != current_user_id:
            raise ValueError("You can only update your own comments")
        db_comment.content = comment.content
        await db.commit()
        await db.refresh(db_comment)
    return db_comment

async def delete_comment(db: AsyncSession, comment_id: int):
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
    return db_comment

async def get_comments_by_post(db: AsyncSession, post_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_comments_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Comment).filter(Comment.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_comments_by_post_and_user(db: AsyncSession, post_id: int, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Comment).filter(Comment.post_id == post_id, Comment.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()
