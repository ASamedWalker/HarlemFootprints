from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List


class ContributionCreate(BaseModel):
    historical_site_id: int
    contributor_name: str
    contribution_details: str
    images: Optional[List[HttpUrl]] = []
    audio: Optional[HttpUrl] = None
    verified: bool = False

    class Config:
        from_attributes = True
        json_encoders = {HttpUrl: lambda v: str(v)}

    @validator("images", each_item=True)
    def convert_images_to_str(cls, v):
        return str(v)

    @validator("audio", always=True)
    def convert_audio_to_str(cls, v):
        return str(v) if v else None


class ContributionRead(BaseModel):
    id: int
    historical_site_id: int
    contributor_name: str
    contribution_details: str
    images: List[HttpUrl]
    audio: Optional[HttpUrl]
    verified: bool

    class Config:
        from_attributes = True


class ContributionUpdate(BaseModel):
    contributor_name: Optional[str]
    contribution_details: Optional[str]
    images: Optional[List[HttpUrl]]
    audio: Optional[HttpUrl]
    verified: Optional[bool]

    class Config:
        from_attributes = True
        json_encoders = {HttpUrl: lambda v: str(v)}

    @validator("images", each_item=True)
    def convert_images_to_str(cls, v):
        return str(v)

    @validator("audio", always=True)
    def convert_audio_to_str(cls, v):
        return str(v) if v else None


class ContributionDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
