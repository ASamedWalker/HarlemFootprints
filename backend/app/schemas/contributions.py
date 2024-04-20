from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class ContributionCreate(BaseModel):
    site_id: int
    user_id: int  # Assuming users are identified by an ID
    text: str
    images: Optional[List[HttpUrl]] = []
    audio: Optional[HttpUrl] = None
    verified: bool = False  # Contributions might need verification

    class Config:
        orm_mode = True


class ContributionRead(BaseModel):
    id: int
    site_id: int
    user_id: int
    text: str
    images: List[HttpUrl] = []
    audio: Optional[HttpUrl] = None
    verified: bool

    class Config:
        from_attributes = True


class ContributionUpdate(BaseModel):
    text: Optional[str] = None
    images: Optional[List[HttpUrl]] = None
    audio: Optional[HttpUrl] = None
    verified: Optional[bool] = None

    class Config:
        from_attributes = True


class ContributionDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
