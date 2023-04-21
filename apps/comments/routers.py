from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.comments.schemas import CommentBase, CommentList
from apps.comments.crud import comment
from apps.users.db import User
from utils.deps import get_db, get_current_user

router = APIRouter(
    tags=['comments']
)


@router.post(
    "/",
)
def create_comment(
        item: CommentBase,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.id != item.user_id:
        raise HTTPException(
            status_code=400,
            detail="you are not owner"
        )
    return comment.create(db=db, obj_in=item)


@router.put(
    path="/",
    response_model=CommentList
)
def update_comment(
        update_item: CommentBase,
        model_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.id != update_item.user_id:
        raise HTTPException(
            status_code=400,
            detail="you are not owner"
        )
    item = comment.get(db=db, model_id=model_id)
    return comment.update(db=db, db_obj=item, obj_in=update_item)


@router.delete(
    path="/",
)
def delete_comment(
        model_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    comment_obj = comment.get(db=db, model_id=model_id)
    post_owner_id = comment_obj.post.owner
    if current_user.id != comment_obj.user_id or post_owner_id != comment_obj.user_id:
        raise HTTPException(
            status_code=400,
            detail="you are not owner"
        )
    return comment.remove(db=db, model_id=comment_obj.id)
