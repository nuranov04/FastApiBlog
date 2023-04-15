from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.users.db import User
from apps.likes.crud import like
from apps.likes.schemas import (
    LikeList,
    LikeCreate,
    LikeDetail,
)
from utils.deps import get_db, get_current_user
from apps.posts import post
router = APIRouter(
    tags=['likes']
)


@router.get("/post")
def get_post_likes_list(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return like.get_post_likes(db=db, post_id=post_id)


@router.get("/user")
def get_post_user_likes(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if user_id == current_user.id:
        return current_user.likes
    raise HTTPException(
        status_code=400,
        detail="it's not your profile"
    )


@router.post("", response_model=LikeDetail)
def create_like(
    item: LikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="it's not your id"
        )
    if post.get(db=db, model_id=item.post_id) is None:
        raise HTTPException(
            status_code=400,
            detail="post not found"
        )
    if like.check_like_in_db(db=db, user_id=item.user_id, post_id=item.post_id):
        raise HTTPException(
            status_code=400,
            detail="Already exist"
        )
    return like.create(db=db, obj_in=item)


@router.delete("")
def delete_like(
        user_id: int,
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="It is not your like"
        )
    if like.check_like_in_db(db=db, user_id=user_id, post_id=post_id):
        return like.remove(db=db, model_id=like.get_by_user_id_and_post_id(db=db, user_id=user_id, post_id=post_id).id)
    raise HTTPException(
        status_code=400,
        detail="Like not found"
    )
