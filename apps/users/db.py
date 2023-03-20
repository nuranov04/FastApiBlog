from sqlalchemy import Column, Boolean, Integer, String, Text

from core.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    fullname = Column(String)
    bio = Column(Text)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
