from pydantic import BaseModel


class FollowerBase(BaseModel):
    owner: int
    to_user: int

    class Config:
        orm_mode = True


class FollowerList(FollowerBase):
    id: int
