from pydantic import BaseModel
from typing import List, Optional


class HistoricalEventCreate(BaseModel):
    title: str
    description: str
    date: str
    site_id: int
    participants: List[str] = []
    event_type: str
    images: List[str] = []


class HistoricalEventRead(HistoricalEventCreate):
    id: int


class HistoricalEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    site_id: Optional[int] = None
    participants: Optional[List[str]] = None
    event_type: Optional[str] = None
    images: Optional[List[str]] = None


class HistoricalEventDelete(BaseModel):
    id: int
