from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlmodel import SQLModel, Field
from typing import List, Optional


class HistoricalSite(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(String, unique=True, index=True)
    )  # Correct way to set unique and index
    description: str = Field(sa_column=Column(String))
    latitude: float = Field(sa_column=Column(Float))
    longitude: float = Field(sa_column=Column(Float))
    address: str = Field(
        default=None, sa_column=Column(String, nullable=True)
    )  # Here nullable is set directly
    era: str = Field(sa_column=Column(String))
    tags: List[str] = Field(
        default=[], sa_column=Column(JSON)
    )  # JSON column for storing lists
    images: List[str] = Field(
        default=[], sa_column=Column(JSON)
    )  # JSON column for storing lists
    audio_guide_url: Optional[str] = Field(
        default=None, sa_column=Column(String, nullable=True)
    )
    verified: bool = Field(default=False, sa_column=Column(Boolean))
