from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.contributions_service import (
    create_contribution,
    get_contribution_by_id,
    get_all_contributions,
    update_contribution,
    delete_contribution,
)
from schemas.contributions import (
    ContributionCreate,
    ContributionUpdate,
    ContributionRead,
)
from data.database import get_session

router = APIRouter()


@router.post("/", response_model=ContributionCreate)
async def create_contribution_endpoint(
    contribution: ContributionCreate, db: AsyncSession = Depends(get_session)
):
    return await create_contribution(db, contribution)


@router.get("/", response_model=list[ContributionRead])
async def get_all_contributions_endpoint(db: AsyncSession = Depends(get_session)):
    return await get_all_contributions(db)


@router.get("/{id}", response_model=ContributionUpdate)
async def get_contribution_endpoint(id: int, db: AsyncSession = Depends(get_session)):
    return await get_contribution_by_id(db, id)


@router.put("/{id}", response_model=ContributionUpdate)
async def update_contribution_endpoint(
    id: int, contribution: ContributionUpdate, db: AsyncSession = Depends(get_session)
):
    return await update_contribution(db, id, contribution)


@router.delete("/{id}", response_model=bool)
async def delete_contribution_endpoint(
    id: int, db: AsyncSession = Depends(get_session)
):
    return await delete_contribution(db, id)


# Compare this snippet from backend/app/models/contributions.py:
# from sqlmodel import Field, SQLModel
#
#
# class UserContribution(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     contributor_name: str
#     contribution_details: str
#     historical_site_id: int
