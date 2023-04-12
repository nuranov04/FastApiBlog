from sqlalchemy import Column, Integer, Text, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    title = Column(String(length=256))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="posts")
    images = relationship("PostImage", back_populates="post")


class PostImage(Base):
    __tablename__ = "post_image"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    image = Column(String)
    post_id = Column(Integer, ForeignKey("post.id"))

    post = relationship("Post", back_populates="images")
