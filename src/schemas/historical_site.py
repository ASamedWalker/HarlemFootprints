from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Schema for client inputs on creating a new historical site
class HistoricalSiteCreate(BaseModel):
    name: str
    description: str
    longitude: float
    latitude: float
    address: Optional[str]
    era: str
    tags: List[str]
    images: List[str]
    audio_guide_url: Optional[str]


# Schema for responses, this might include fields like creation date or other auto-generated data
class HistoricalSiteRead(HistoricalSiteCreate):
    id: int
    verified: bool = False

    class Config:
        from_attributes = True


class HistoricalSiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    address: Optional[str] = None
    era: Optional[str] = None
    tags: Optional[List[str]] = None
    images: Optional[List[str]] = None
    audio_guide_url: Optional[str] = None
    verified: Optional[bool] = None

    class Config:
        from_attributes = True


class HistoricalSiteDelete(BaseModel):
    id: int
