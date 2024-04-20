from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from models.contributions import UserContribution
from schemas.contributions import ContributionCreate, ContributionUpdate


async def create_contribution(
    db: AsyncSession, contribution_data: ContributionCreate
) -> UserContribution:
    """
    Create a new contribution entry in the database.
    """
    new_contribution = UserContribution(**contribution_data.dict())
    db.add(new_contribution)
    try:
        await db.commit()
        await db.refresh(new_contribution)
        return new_contribution
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_contribution_by_id(
    db: AsyncSession, contribution_id: int
) -> UserContribution:
    """
    Retrieve a contribution by its ID.
    """
    query = select(UserContribution).where(UserContribution.id == contribution_id)
    result = await db.execute(query)
    contribution = result.scalars().first()
    if contribution:
        return contribution
    else:
        raise HTTPException(status_code=404, detail="Contribution not found")


async def update_contribution(
    db: AsyncSession, contribution_id: int, update_data: ContributionUpdate
) -> UserContribution:
    """
    Update an existing contribution.
    """
    contribution = await get_contribution_by_id(db, contribution_id)
    for var, value in update_data.dict(exclude_unset=True).items():
        setattr(contribution, var, value)
    try:
        await db.commit()
        return contribution
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_contribution(db: AsyncSession, contribution_id: int) -> bool:
    """
    Delete a contribution from the database.
    """
    contribution = await get_contribution_by_id(db, contribution_id)
    if contribution:
        try:
            await db.delete(contribution)
            await db.commit()
            return True
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Contribution not found")
