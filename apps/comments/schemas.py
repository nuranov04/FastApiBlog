from pydantic import BaseModel


class CommentBase(BaseModel):
    post_id: int
    user_id: int
    comment: str


class CommentList(CommentBase):
    id: int

