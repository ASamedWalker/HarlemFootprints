from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContributionCreate(BaseModel):
    user_id: int
    site_id: int
    content: str
    contribution_type: str
    created_at: datetime
    approved: bool


class ContributionRead(ContributionCreate):
    id: int


class ContributionUpdate(BaseModel):
    user_id: Optional[int] = None
    site_id: Optional[int] = None
    content: Optional[str] = None
    contribution_type: Optional[str] = None
    created_at: Optional[datetime] = None
    approved: Optional[bool] = None


class ContributionDelete(BaseModel):
    id: int
