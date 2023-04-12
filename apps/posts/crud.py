from typing import Optional, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from utils import CRUDBase
from .db import Post, PostImage
from .schemas import (
    PostImageBase,
    PostImageInPost,
    PostImageCreate,
    PostImageUpdate,
    PostBase,
    PostList,
    PostCreate,
    PostUpdate,
)
from ..users import user


class PostCrud(CRUDBase[Post, PostCreate, PostUpdate]):

    def get_all_user_posts(self, db: Session, user_id: int):
        return db.query(Post).filter(Post.owner_id == user_id)

    def create(self, db: Session, *, obj_in: PostCreate) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        user_obj = user.get(db=db, model_id=obj_in_data["owner"].id)
        if user_obj:
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj


class PostImageCrud(CRUDBase[PostImage, PostImageCreate, PostImageUpdate]):

    def get_post_images(self, db: Session, post_id: int):
        return db.query(PostImage).filter(PostImage.post_id == post_id)


post = PostCrud(Post)
post_image = PostImageCrud(PostImage)
