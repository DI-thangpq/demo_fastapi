from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.comment import create_comment, get_comments, update_comment
from app.database import get_db
from app.models.user import User
from app.schemas.comment import Comment, CommentPatch
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[Comment])
async def read_comments(skip: int=0, limit: int=100, db:AsyncSession=Depends(get_db)):
    comments = await get_comments(db, skip=skip, limit=limit)
    return comments

@router.post("/", response_model=Comment)
async def create_comment_route(comment: Comment, db:AsyncSession=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        current_user_obj = await current_user  # Await the coroutine to get the User object
        return await create_comment(db, comment, current_user_obj.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{comment_id}", response_model=Comment)
async def update_comment_route(comment_id: int, comment: CommentPatch, db:AsyncSession=Depends(get_db), current_user: User=Depends(get_current_user)):
    try:
        current_user_obj = await current_user  # Await the coroutine to get the User object
        db_comment = await update_comment(db, comment_id, comment, current_user_obj.id)
        if db_comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return db_comment
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))