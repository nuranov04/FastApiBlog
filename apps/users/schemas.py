from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, validator, Field


class BaseUser(BaseModel):
    fullname: str
    username: str
    bio: str
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class UserList(BaseUser):
    id: int
    date: date


class UserDetail(UserList):
    is_active: bool = False
    is_admin: bool = False
    date: date


class UserCreateUpdate(BaseUser):
    password: str = Field(..., min_length=8, description="password must be less then 8 characters")

    # @validator("password")
    # def check_password(self, value):
    #     if len(value) < 8:
    #         raise ValueError("password must be less then 8 characters")


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
