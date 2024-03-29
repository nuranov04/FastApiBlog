from datetime import date

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from utils.base_CRUD import CRUDBase
from .db import Post, PostImage
from .schemas import (
    PostImageCreate,
    PostImageUpdate,
    PostCreate,
    PostUpdate,
)
from apps.users.routers import user


class PostCrud(CRUDBase[Post, PostCreate, PostUpdate]):

    def get_all_user_posts(self, db: Session, user_id: int):
        return db.query(Post).filter_by(owner_id=user_id)

    def get_multi(self, db: Session):
        return db.query(Post)

    def create(
            self,
            db: Session,
            *,
            obj_in: PostCreate,
            user_id: int
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        user_obj = user.get(db=db, model_id=user_id)

        obj_in_data['created_at'] = date.today()
        obj_in_data['owner_id'] = user_id

        if user_obj:
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj


class PostImageCrud(CRUDBase[PostImage, PostImageCreate, PostImageUpdate]):

    def get_post_images(self, db: Session, post_id: int):
        return db.query(PostImage).filter(PostImage.post_id == post_id).all()


post = PostCrud(Post)
post_image = PostImageCrud(PostImage)
