from typing import Any, Dict, Optional, Union
from datetime import date

from sqlalchemy.orm import Session

from apps.users import User, UserCreateUpdate
from core.security import get_hashed_password, verify_password
from utils import CRUDBase


class UserCruD(CRUDBase[User, UserCreateUpdate, UserCreateUpdate]):

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def get_user_by_id(self, db: Session, *, user_id: str) -> Optional[User]:
        return db.query(User).filter_by(id=user_id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter_by(email=email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        obj = db.query(User).filter_by(username=username).first()
        return obj

    def create(self, db: Session, *, obj_in: UserCreateUpdate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_hashed_password(obj_in.password),
            fullname=obj_in.fullname,
            date=date.today(),
            username=obj_in.username,
            bio=obj_in.bio
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserCreateUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_hashed_password(update_data['password'])
            update_data["password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

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


user = UserCruD(User)
