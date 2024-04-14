from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class Contribution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    site_id: int = Field(foreign_key="historicalsite.id")
    content: str
    contribution_type: str
    created_at: datetime
    approved: bool = Field(default=False)
    # Relationships
    user: Optional["User"] = Relationship(back_populates="contributions")
    site: Optional["HistoricalSite"] = Relationship(back_populates="contributions")
