from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CommentCreate(BaseModel):
    user_id: int
    site_id: Optional[int]
    event_id: Optional[int]
    content: str
    created_at: datetime


class CommentRead(CommentCreate):
    id: int


class CommentUpdate(BaseModel):
    user_id: Optional[int] = None
    site_id: Optional[int] = None
    event_id: Optional[int] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None


class CommentDelete(BaseModel):
    id: int
