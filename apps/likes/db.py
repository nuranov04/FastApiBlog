from sqlalchemy import (
    Column,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import relationship

from core.db import Base


class Like(Base):
    __tablename__ = "like"

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True
    )
    post_id = Column(Integer, ForeignKey("post.id"))

    user_id = Column(Integer, ForeignKey("user.id"))

    post = relationship("Post", backref="post_likes")

    user = relationship("User", backref="user_likes", viewonly=True)
