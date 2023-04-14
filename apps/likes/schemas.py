from pydantic import BaseModel


class BaseLike(BaseModel):
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class LikeList(BaseLike):
    id: int


class LikeDetail(LikeList):
    pass


class LikeCreate(BaseLike):
    pass


class LikeUpdate(BaseLike):
    pass
