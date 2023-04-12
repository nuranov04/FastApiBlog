from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils import get_db, get_current_user
from .schemas import (
    PostImageBase,
    PostImageInPost,
    PostImageCreate,
    PostBase,
    PostDetail,
    PostList,
    PostCreate,
    PostUpdate
)
from .crud import post, post_image

routers = APIRouter(
    tags=["posts"]
)


@routers.get("/", response_model=List[PostList])
def get_post_list(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_posts = post.get_all_user_posts(db=db, user_id=current_user.id)
    return user_posts


@routers.get("/{id}", response_model=PostDetail)
def get_post(model_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post_obj = post.get(db=db, model_id=model_id)
    if post_obj.owner_id != current_user.id:
        return HTTPException(
            status_code=400,
            detail="Your are not owner"
        )
    post_image_obj = post_image.get_post_images(db=db, post_id=model_id)
    setattr(post_obj, "image", post_image_obj)
    return post_obj


@routers.post("/", response_model=PostCreate)
def create_post(
        item: PostCreate,
        db: Session = Depends(get_db),
):
    return post.create(db=db, obj_in=item)


@routers.post("/", response_model=PostUpdate)
def update_post(
        model_id: int,
        update_item: PostUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    post_obj = post.get(db=db, model_id=model_id)
    if current_user.id == post_obj.owner_id:
        return post.update(db=db, db_obj=post_obj, obj_in=update_item)
    return HTTPException(
        status_code=400,
        detail="You are not owner of post"
    )


@routers.delete("/", response_model=PostCreate)
def delete_post(
        model_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    post_obj = post.get(db, model_id)
    if post_obj.owner_id == current_user.id:
        return post.remove(db, model_id=model_id)
    return HTTPException(
        status_code=400,
        detail="You are not owner of post"
    )
