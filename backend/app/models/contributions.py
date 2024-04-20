from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime


class UserContribution(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    contributor_name: str
    contribution_details: str
    historical_site_id: int = Field(default=None, foreign_key="historicalsite.id")
    historical_site: "HistoricalSite" = Relationship(back_populates="contributions")

