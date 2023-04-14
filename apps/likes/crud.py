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


like = LikeCrud(Like)
