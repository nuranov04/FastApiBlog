from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    fullname: str
    username: str
    bio: str
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class UserList(BaseUser):
    id: int


class UserDetail(UserList):
    is_active: bool = False
    is_admin: bool = False


class UserCreateUpdate(BaseUser):
    password: str
