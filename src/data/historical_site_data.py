from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from models.historical_site import HistoricalSite
from schemas.historical_site import HistoricalSiteCreate, HistoricalSiteRead
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def create_historical_site(
    db: AsyncSession, site: HistoricalSiteCreate
) -> HistoricalSite:
    new_site = HistoricalSite(**site.model_dump())
    try:
        db.add(new_site)
        logger.info(f"Creating new historical site: {new_site}")
        await db.commit()
        logger.info(f"New historical site created: {new_site}")
        await db.refresh(new_site)
        return new_site
    except IntegrityError as e:
        logger.error(f"An error occurred when creating the historical site: {e}")
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"An error occurred when creating the historical site: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_historical_site(db: AsyncSession, site_id: int) -> HistoricalSite:
    try:
        query = select(HistoricalSite).filter(HistoricalSite.id == site_id)
        result = await db.execute(query)
        return result.scalars().one()
    except NoResultFound as e:
        logger.error(f"An error occurred when getting the historical site: {e}")
        raise HTTPException(status_code=404, detail="Historical site not found")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred when getting the historical site: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_historical_sites(db: AsyncSession) -> list:
    try:
        query = select(HistoricalSite)
        result = await db.execute(query)
        return result.scalars().all()
    except NoResultFound as e:
        logger.error(f"An error occurred when getting all historical sites: {e}")
        raise HTTPException(status_code=404, detail="No historical sites found")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred when getting all historical sites: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def update_historical_site(
    session: AsyncSession, site_id: int, update_data: dict
) -> Optional[HistoricalSiteRead]:
    # Validate update_data
    if not isinstance(update_data, dict):
        raise HTTPException(
            status_code=400, detail="Update data must be a dictionary"
        )
    for key in update_data:
        if not hasattr(HistoricalSite, key):
            raise HTTPException(status_code=400, detail=f"Invalid key: {key}")

    try:
        historical_site = await session.get(HistoricalSite, site_id)
        if not historical_site:
            raise HTTPException(status_code=404, detail="Historical site not found")

        for key, value in update_data.items():
            setattr(historical_site, key, value)

        await session.commit()
        return historical_site  # Assuming model_dump() is not required or is handled elsewhere

    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Failed to update historical site due to constraint violation: {e}")
        raise HTTPException(
            status_code=400,
            detail="Failed to update historical site due to constraint violation"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Failed to update historical site: {e}")
        raise HTTPException(status_code=500, detail="A database error occurred")


async def delete_historical_site(db: AsyncSession, site_id: int) -> bool:
    site = await get_historical_site(db, site_id)
    if site:
        await db.delete(site)
        await db.commit()
        return True
    return False
