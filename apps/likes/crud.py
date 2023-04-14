from typing import List

from sqlalchemy.orm import Session

from utils import CRUDBase
from apps.likes import Like
from .schemas import LikeCreate, LikeUpdate


class LikeCrud(CRUDBase[Like, LikeCreate, LikeUpdate]):

    def get_post_likes(
            self, db: Session,
            post_id: int
    ) -> List[Like]:
        return db.query(Like).filter(Like.post_id == post_id).all()

    def get_user_likes(
            self, db: Session,
            user_id: int
    ) -> List[Like]:
        return db.query(Like).filter(Like.user_id == user_id).all()

    def get_by_user_id_and_post_id(
            self, db: Session,
            user_id: int,
            post_id: int
    ):
        return db.query(Like).filter_by(user_id=user_id, post_id=post_id).first()

    def check_like_in_db(
            self, db: Session,
            user_id: int,
            post_id: int
    ) -> bool:
        if self.get_by_user_id_and_post_id(db=db, user_id=user_id, post_id=post_id) is None:
            return False
        return True


like = LikeCrud(Like)
