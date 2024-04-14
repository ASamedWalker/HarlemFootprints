from pydantic import BaseModel
from typing import List, Optional, Any, Dict


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
    verified: bool

    class Config:
        from_attributes = True


# Schema for updates, usually optional fields, as not all fields need to be updated
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


class HistoricalSiteDelete(BaseModel):
    id: int
