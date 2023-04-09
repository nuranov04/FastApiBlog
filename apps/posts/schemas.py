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


class PostImageInPost(PostImageBase):
    image: str


class PostList(PostBase):
    id: int
    owner: UserDetail
    post_images: List[PostImageInPost] = None


class PostImageCreate(PostImageInPost):
    post: PostList


class PostCreate(PostBase):
    id: int
    owner: UserDetail


class PostUpdate(PostBase):
    pass
