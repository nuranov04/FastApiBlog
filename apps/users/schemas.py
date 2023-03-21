from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    fullname: str
    username: str
    bio: str
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class UserList(BaseUser):
    date: date
    id: int


class UserDetail(UserList):
    date: date
    is_active: bool = False
    is_admin: bool = False


class UserCreateUpdate(BaseUser):
    password: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
