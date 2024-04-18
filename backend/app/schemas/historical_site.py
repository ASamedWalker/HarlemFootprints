from pydantic import BaseModel
from typing import List, Optional


# Schema for client inputs on creating a new historical site
class HistoricalSiteCreate(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    era: str
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []
    audio_guide_url: Optional[str] = None
    verified: Optional[bool] = False


# Schema for responses, which might include additional fields like creation date or other auto-generated data
class HistoricalSiteRead(HistoricalSiteCreate):
    id: int

    class Config:
        from_attributes = True


# Schema for updates, usually includes optional fields as not all fields need to be updated
class HistoricalSiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    era: Optional[str] = None
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []
    audio_guide_url: Optional[str] = None
    verified: Optional[bool] = None
