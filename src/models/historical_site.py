from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON
from sqlalchemy import Column
from typing import List, Optional


class HistoricalSite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    longitude: float
    latitude: float
    address: Optional[str] = Field(index=True)
    era: str
    tags: List[str] = Field(sa_column=Column(JSON), default=[])
    images: List[str] = Field(sa_column=Column(JSON), default=[])
    audio_guide_url: Optional[str]
    verified: bool = Field(default=False)
    # Relationships
    events: List["HistoricalEvent"] = Relationship(back_populates="site")
    contributions: List["Contribution"] = Relationship(back_populates="site")
    comments: List["Comment"] = Relationship(back_populates="site")
