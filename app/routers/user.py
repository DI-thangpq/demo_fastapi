from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import get_users, get_user, create_user as crud_create_user, delete_user
from app.database import get_db
from app.utils.security import get_current_user
from app.models.user import User, Role
from app.schemas.user import UserCreate, User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN.value:
        raise HTTPException(status_code=status.HTTP403_FORBIDDEN, detail="Only admin can perform this action")
    return current_user

@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_create_user(db=db, user=user)
    return db_user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=User, dependencies=[Depends(is_admin)])
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user