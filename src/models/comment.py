from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    site_id: Optional[int] = Field(default=None, foreign_key="historicalsite.id")
    event_id: Optional[int] = Field(default=None, foreign_key="historicalevent.id")
    content: str
    created_at: datetime
    # Relationships
    user: Optional["User"] = Relationship(back_populates="comments")
    site: Optional["HistoricalSite"] = Relationship(back_populates="comments")
    event: Optional["HistoricalEvent"] = Relationship(back_populates="comments")
