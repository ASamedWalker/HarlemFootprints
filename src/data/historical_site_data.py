from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from src.models.historical_site import HistoricalSite
from src.schemas.historical_site import HistoricalSiteCreate, HistoricalSiteUpdate
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
    db: AsyncSession, site_id: int, update: HistoricalSiteUpdate
) -> HistoricalSite:
    try:
        query = select(HistoricalSite).filter(HistoricalSite.id == site_id)
        result = await db.execute(query)
        scalars = result.scalars()  # Do not await the scalars() call
        site = scalars.one()  # Do not await the one() call
        for key, value in update.dict(exclude_unset=True).items():
            setattr(site, key, value)
        await db.commit()
        await db.refresh(site)
        return site
    except NoResultFound as e:
        logger.error(f"An error occurred when updating the historical site: {e}")
        raise HTTPException(status_code=404, detail="Historical site not found")
    except IntegrityError as e:
        logger.error(f"An error occurred when updating the historical site: {e}")
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"An error occurred when updating the historical site: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_historical_site(db: AsyncSession, site_id: int) -> bool:
    site = await get_historical_site(db, site_id)
    if site:
        await db.delete(site)
        await db.commit()
        return True
    return False
