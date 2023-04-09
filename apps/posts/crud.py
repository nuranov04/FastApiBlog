from typing import Optional

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


class PostCrud(CRUDBase[Post, PostCreate, PostUpdate]):

    def get_all_user_posts(self, db: Session, user_id: int) -> Optional[Post]:
        return db.query(Post).filter(Post.owner_id == user_id)


class PostImageCrud(CRUDBase[PostImage, PostImageCreate, PostImageUpdate]):

    def get_post_images(self, db: Session, post_id: int) -> Optional[PostImage]:
        return db.query(PostImage).filter(PostImage.post_id == post_id)


post = PostCrud(Post)
post_image = PostImageCrud(PostImage)
