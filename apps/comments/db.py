from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text
)
from sqlalchemy.orm import relationship

from core.db import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True
    )
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)

    post = relationship("Post", backref="post_comments")

    user = relationship("User", backref="user_comments", viewonly=True)
