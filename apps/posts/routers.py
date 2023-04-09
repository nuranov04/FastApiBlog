from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils import get_db, get_current_user
from .db import Post, PostImage
from .schemas import (
    PostImageBase,
    PostImageInPost,
    PostImageCreate,
    PostBase,
    PostList,
    PostCreate
)
from .crud import post, post_image

routers = APIRouter(
    tags=["posts"]
)


@routers.get("/", response_model=List[PostList])
def get_post_list(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_posts = post.get_all_user_posts(db=db, user_id=current_user.id)
    return user_posts

