from typing import List
from pydantic import BaseModel

from apps.users import UserDetail


class PostImageBase(BaseModel):
    id: str

    class Config:
        orm_mode = True


class PostImageUpdate(PostImageBase):
    image: str


class PostBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class PostImageInPost(PostImageBase):
    image: str


class PostList(PostBase):
    id: int
    # owner_id: int


class PostDetail(PostList):
    image: PostImageInPost


class PostImageCreate(PostImageInPost):
    post: PostList


class PostCreate(PostBase):
    owner: UserDetail


class PostUpdate(PostBase):
    pass
