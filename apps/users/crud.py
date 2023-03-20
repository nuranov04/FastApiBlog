from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from apps.users.db import User
from apps.users.schemas import UserCreateUpdate
from core.security import get_password_hash, verify_password
from utils.base_CRUD import CRUDBase


class UserCruD(CRUDBase[User, UserCreateUpdate, UserCreateUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query()