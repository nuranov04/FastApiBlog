from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship
from core.db import Base


class Follower(Base):
    __tablename__ = "follower"

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True
    )

    owner_id = Column(Integer, ForeignKey("user.id"))
    to_user_id = Column(Integer, ForeignKey("user.id"))

    created_at = Column(DateTime, default=datetime.now())

    owner = relationship("User", back_populates="followers")
    to_user = relationship("User", back_populates="subcs")