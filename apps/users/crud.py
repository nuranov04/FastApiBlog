from datetime import date
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.users.db import User
from apps.users.schemas import UserCreateUpdate
from core.security import get_hashed_password, verify_password
from utils.base_CRUD import CRUDBase


class UserCrud(CRUDBase[User, UserCreateUpdate, UserCreateUpdate]):

    def get_by_email(self, db: Session, *, email: str):
        obj = db.query(User).filter_by(email=email).first()
        return obj

    def get_by_username(self, db: Session, *, username: str):
        return db.query(User).filter_by(username=username).first()

    def create(self, db: Session, *, obj_in: UserCreateUpdate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date'] = date.today()
        obj_in_data['password'] = get_hashed_password(obj_in_data['password'])
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_password(
            self,
            db: Session,
            *,
            user_obj: User,
            old_password: str,
            new_password: str
    ) -> User:
        user_obj = self.get(db=db, model_id=user_obj.id)
        hashed_password = get_hashed_password(old_password)
        if user_obj.password == hashed_password:
            setattr(user_obj, "password", get_hashed_password(new_password))

        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    def authenticated(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user_obj = self.get_by_username(db, username=username)
        if user_obj is None:
            return None
        if not verify_password(password, user_obj.password):
            return None
        return user_obj

    def is_active(self, user_obj: User) -> bool:
        return user_obj.is_active

    def is_admin(self, user_obj: User) -> bool:
        return user_obj.is_admin


user = UserCrud(User)
