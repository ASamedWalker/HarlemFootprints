from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime



class ContributionCreate(BaseModel):
    user_id: int
    site_id: int
    content: str
    contribution_type: str
    created_at: datetime
    approved: bool


class ContributionUpdate(BaseModel):
    user_id: Optional[int]
    site_id: Optional[int]
    content: Optional[str]
    contribution_type: Optional[str]
    created_at: Optional[datetime]
    approved: Optional[bool]


class ContributionRead(BaseModel):
    id: int
    user_id: int
    site_id: int
    content: str
    contribution_type: str
    created_at: datetime
    approved: bool

   Config: ConfigDict = {"from_attributes": True}

class ContributionDelete(BaseModel):
    id: int
    user_id: int
    site_id: int
    content: str
    contribution_type: str
    created_at: datetime
    approved: bool
