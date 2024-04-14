from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.historical_site import HistoricalSite
from ..schemas.historical_site import HistoricalSiteCreate, HistoricalSiteUpdate


async def create_historical_site(
    db: AsyncSession, site: HistoricalSiteCreate
) -> HistoricalSite:
    new_site = HistoricalSite(**site.dict())
    db.add(new_site)
    await db.commit()
    await db.refresh(new_site)
    return new_site


async def get_historical_site(db: AsyncSession, site_id: int) -> HistoricalSite:
    query = select(HistoricalSite).where(HistoricalSite.id == site_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_all_historical_sites(db: AsyncSession) -> list:
    query = select(HistoricalSite)
    result = await db.execute(query)
    return result.scalars().all()


async def update_historical_site(
    db: AsyncSession, site_id: int, update: HistoricalSiteUpdate
) -> HistoricalSite:
    site = await get_historical_site(db, site_id)
    if site:
        update_data = update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(site, key, value)
        await db.commit()
        await db.refresh(site)
        return site
    return None


async def delete_historical_site(db: AsyncSession, site_id: int) -> bool:
    site = await get_historical_site(db, site_id)
    if site:
        await db.delete(site)
        await db.commit()
        return True
    return False
