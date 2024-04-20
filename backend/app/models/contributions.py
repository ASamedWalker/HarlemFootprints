from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from datetime import datetime
from typing import List, Optional


# Import JSON type
class UserContribution(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    # New fields
    images: List[str] = Field(default=[], sa_column=Column(JSON))  # Store image URLs
    audio: Optional[str] = Field(
        default=None, sa_column=Column(String)
    )  # URL to audio file
    verified: bool = Field(
        default=False, sa_column=Column(Boolean)
    )  # Whether the contribution is verified
    contributor_name: str
    contribution_details: str
    historical_site_id: int = Field(default=None, foreign_key="historicalsite.id")
    historical_site: "HistoricalSite" = Relationship(back_populates="contributions")
