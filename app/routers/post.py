from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.post import get_posts, get_post, create_post, update_post
from app.database import get_db
from app.schemas.post import Post, PostCreate, PostUpdate
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[Post])
async def read_posts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    posts = await get_posts(db, skip=skip, limit=limit)
    return posts

@router.post("/", response_model=Post)
async def create_post_route(post: PostCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        current_user_obj = await current_user  # Await the coroutine to get the User object
        return await create_post(db, post, current_user_obj.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=Post)
async def update_post_route(post_id: int, post: PostUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user_obj = await current_user  # Await the coroutine to get the User object
    db_post = await update_post(db, post_id, post, current_user_obj.id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post