from sqlalchemy import Column, Integer, Text, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    title = Column(String(length=256))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("user", back_populates="posts")


class PostImage(Base):
    __tablename__ = "post_image"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    post_id = Column(String, ForeignKey("post.id"))
    post = relationship("post", back_populates="post_image")
    image = Column(String)
