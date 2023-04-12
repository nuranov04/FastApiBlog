from datetime import date

from sqlalchemy import Column, Boolean, Integer, String, Text, Date
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    fullname = Column(String)
    bio = Column(Text)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    date = Column(Date, default=date.today())
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
