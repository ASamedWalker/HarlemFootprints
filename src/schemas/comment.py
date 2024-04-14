from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class CommentCreate(BaseModel):
    user_id: int
    site_id: Optional[int]
    event_id: Optional[int]
    content: str
    created_at: datetime


class CommentUpdate(BaseModel):
    user_id: Optional[int]
    site_id: Optional[int]
    event_id: Optional[int]
    content: Optional[str]
    created_at: Optional[datetime]


class CommentRead(BaseModel):
    id: int
    user_id: int
    site_id: Optional[int]
    event_id: Optional[int]
    content: str
    created_at: datetime

    Config: ConfigDict = {"from_attributes": True}


class CommentDelete(BaseModel):
    id: int
    user_id: int
    site_id: Optional[int]
    event_id: Optional[int]
    content: str
    created_at: datetime
