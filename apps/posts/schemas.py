from typing import List

from pydantic import BaseModel

from apps.likes.schemas import LikeList


class PostImageBase(BaseModel):
    image: str

    class Config:
        orm_mode = True


class PostImageUpdate(PostImageBase):
    id: int


class PostBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class PostImageInPost(PostImageBase):
    id: int
    post_id: int


class PostList(PostBase):
    id: int
    owner_id: int


class PostImageCreate(PostImageBase):
    post_id: int


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostDetail(PostList):
    image: List[PostImageInPost]
    likes_count: int
    likes: List[LikeList]
