from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from utils import get_db, get_current_user
from .db import User
from .crud import user
from .schemas import (
    BaseUser,
    UserList,
    UserDetail,
    UserCreateUpdate,
    TokenPayload,
    Token
)

router = APIRouter()


@router.get("/", response_model=List[BaseUser], tags=['users'])
def get_user_list(db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    if user.is_admin(current_user):
        return user.get_all_users(db)
    raise HTTPException(
        status_code=400,
        detail="Not enough privileges"
    )


@router.get("/{username}", response_model=UserDetail, tags=['users'], description="Get user by username")
def get_user_by_username(
        username: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    user_obj = user.get_by_username(db=db, username=username)
    if user == current_user:
        return user
    if not user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="Not enough privileges"
        )
    return user_obj


@router.get("/{email}", response_model=UserDetail, tags=["users"], description="Get user by email")
def get_user_by_email(
        email: EmailStr,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    user_obj = user.get_by_email(db, email=email)
    if user_obj == current_user:
        return user_obj
    if not user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="Not enough privileges"
        )
    return user_obj


@router.get("/{id}", response_model=UserDetail)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    user_obj = user.get_user_by_id(db, user_id=user_id)
    if user_obj == current_user:
        return user_obj
    if not user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="Not enough privileges"
        )
    return user_obj


@router.get("/me")
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> User:
    return current_user

