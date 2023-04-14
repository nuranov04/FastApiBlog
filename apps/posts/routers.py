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
from ..users import User

routers = APIRouter(
    tags=["posts"]
)


@routers.get("/", response_model=List[PostList])
def get_post_list(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
        title: str = None,
        owner_id: str | int = None,
        description: str = None
):
    posts = post.get_multi(db=db)
    if title is not None:
        posts = posts.filter_by(title=title)
    if owner_id is not None:
        posts = posts.filter_by(owner_id=owner_id)
    if description is not None:
        posts = posts.filter_by(description=description)
    return posts.all()


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
        current_user: User = Depends(get_current_user)
):
    return post.create(db=db, obj_in=item, user_id=current_user.id)


@routers.patch("/", response_model=PostUpdate)
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


@routers.post("/images", response_model=PostImageInPost)
def create_post_image(item: PostImageCreate,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):

    post_obj = post.get(db=db, model_id=item.post_id)
    if post_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="this is post not your"
        )
    if post_obj is None:
        raise HTTPException(
            status_code=400,
            detail="post not found"
        )
    return post_image.create(db=db, obj_in=item)
