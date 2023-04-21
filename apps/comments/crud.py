from typing import List

from sqlalchemy.orm import Session

from utils.base_CRUD import CRUDBase
from apps.comments.db import Comment
from apps.comments.schemas import CommentBase, CommentList


class CommentCrud(CRUDBase[Comment, CommentBase, CommentList]):

    def get_post_comments(self, db: Session, post_id: int) -> List[Comment]:
        return db.query(Comment).filter_by(post_id=post_id).all()

    def get_user_comments(self, db: Session, user_id: int) -> List[Comment]:
        return db.query(Comment).filter_by(user_id=user_id).all()

    def get_post_comments_count(self, db: Session, post_id: int) -> int:
        return self.get_post_comments(db, post_id).count()


comment = CommentCrud(Comment)
