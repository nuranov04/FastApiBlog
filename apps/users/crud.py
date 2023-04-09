from typing import Optional

from sqlalchemy.orm import Session

from apps.users import User, UserCreateUpdate
from core.security import get_hashed_password, verify_password
from utils import CRUDBase


class UserCrud(CRUDBase[User, UserCreateUpdate, UserCreateUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter_by(email=email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        obj = db.query(User).filter_by(username=username).first()
        return obj

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
