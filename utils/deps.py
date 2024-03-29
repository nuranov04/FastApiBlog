from typing import Generator

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from apps.users.db import User
from apps.users.crud import user
from apps.users.schemas import TokenPayload
from core.config import settings
from core.db import SessionLocal

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(sub=payload['sub'])
    except (jwt.PyJWKError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_obj = user.get_by_email(db, email=token_data.sub)
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj


def get_current_active_token(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
