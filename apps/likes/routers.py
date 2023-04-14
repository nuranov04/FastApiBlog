from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.likes.schemas import (
    LikeList,
    LikeCreate,
    LikeDetail,
    BaseLike
)
from apps.likes import Like, like
from utils import get_db, get_current_user
from apps.users import User

router = APIRouter(
    tags=['likes']
)


@router.get("/")
def get_post_likes_list(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return like.get_post_likes(db=db, post_id=post_id)
