from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    email: Optional[str] = Field(index=True, nullable=True)
    is_admin: bool = Field(default=False)
    # Relationships
    contributions: List["Contribution"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")
