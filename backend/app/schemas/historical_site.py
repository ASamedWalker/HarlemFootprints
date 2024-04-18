from pydantic import BaseModel, validator
from typing import List, Optional
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement
from typing_extensions import Annotated


# Schema for client inputs on creating a new historical site
class HistoricalSiteCreate(BaseModel):
    name: str
    description: str
    location: Optional[Annotated[str, WKBElement]] = None
    address: Optional[str] = None
    era: str
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []
    audio_guide_url: Optional[str] = None
    verified: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True


# Schema for responses, which might include additional fields like creation date or other auto-generated data
class HistoricalSiteRead(HistoricalSiteCreate):
    id: int

    @validator("location", pre=True, always=True)
    def convert_location(cls, v):
        return to_shape(v).wkt if v else None

    class Config:
        arbirary_types_allowed = True
        from_attributes = True


class GeographyUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# Schema for updates, usually includes optional fields as not all fields need to be updated
class HistoricalSiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[GeographyUpdate] = None
    address: Optional[str] = None
    era: Optional[str] = None
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []
    audio_guide_url: Optional[str] = None
    verified: Optional[bool] = None

    class Config:
        arbirary_types_allowed = True
