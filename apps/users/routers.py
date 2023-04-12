from datetime import date
from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from core.security import create_access_token, create_refresh_token
from utils import get_db, get_current_user
from .db import User
from .crud import user
from .schemas import (
    UserList,
    UserDetail,
    Token,
    UserCreateUpdate
)

router = APIRouter(
    tags=["users"]
)


@router.post("/login", tags=["users"], response_model=Token, summary="Create access and refresh token for user")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user_obj = user.authenticated(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    if user_obj is not None:
        return {
            "access_token": create_access_token(user_obj.email),
            "refresh_token": create_refresh_token(user_obj.email)
        }


@router.post("/register", response_model=UserList, tags=["users"], summary="Create new user")
def create_user(user_obj: UserCreateUpdate, db: Session = Depends(get_db)) -> Any:
    user_by_email = user.get_by_email(db, email=user_obj.email)
    if user_by_email is not None:
        raise HTTPException(
            status_code=400,
            detail="email already exist"
        )
    user_by_username = user.get_by_username(db, username=user_obj.username)
    if user_by_username is not None:
        raise HTTPException(
            status_code=400,
            detail="username already exist"
        )
    if len(user_obj.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="password must be less then 8 characters"
        )
    return user.create(db, obj_in=user_obj)


@router.get("/all", response_model=List[UserList], tags=['users'])
def get_user_list(db: Session = Depends(get_db)) -> Any:
    # if user.is_admin(current_user):
    return user.get_multi(db)
    # raise HTTPException(
    #     status_code=400,
    #     detail="Not enough privileges"
    # )


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


@router.get("/{id}", response_model=UserDetail, tags=["users"], description="Get user by id")
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


@router.get("/me", tags=["users"], response_model=UserDetail)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserDetail:
    return current_user
