from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column
from sqlalchemy import JSON
from typing import List, Optional
from datetime import datetime


class HistoricalEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    site_id: Optional[int] = Field(default=None, foreign_key="historicalsite.id")
    participants: List[str] = Field(sa_column=Column(JSON), default=[])
    event_type: str
    images: List[str] = Field(sa_column=Column(JSON), default=[])
    # Relationships
    site: Optional["HistoricalSite"] = Relationship(back_populates="events")
    comments: List["Comment"] = Relationship(back_populates="event")
