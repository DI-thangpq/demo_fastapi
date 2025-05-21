
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.comment import create_comment, get_comments
from app.database import get_db
from app.models.user import User
from app.schemas.comment import Comment
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
