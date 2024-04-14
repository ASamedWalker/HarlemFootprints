from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from data.historical_site_data import (
    create_historical_site as da_create_historical_site,
    get_historical_site as da_get_historical_site,
    get_all_historical_sites as da_get_all_historical_sites,
    update_historical_site as da_update_historical_site,
    delete_historical_site as da_delete_historical_site,
)
from schemas.historical_site import (
    HistoricalSiteCreate,
    HistoricalSiteRead,
    HistoricalSiteUpdate,
    HistoricalSiteDelete,
)


async def create_historical_site(
    db: AsyncSession, site: HistoricalSiteCreate
) -> HistoricalSiteRead:
    new_site = await da_create_historical_site(db, site)
    return HistoricalSiteRead.from_orm(new_site)


async def get_historical_site(db: AsyncSession, site_id: int) -> HistoricalSiteRead:
    site = await da_get_historical_site(db, site_id)
    if site:
        return HistoricalSiteRead.from_orm(site)
    return None


async def get_all_historical_sites(db: AsyncSession) -> List[HistoricalSiteRead]:
    sites = await da_get_all_historical_sites(db)
    return [HistoricalSiteRead.from_orm(site) for site in sites]


async def update_historical_site(
    db: AsyncSession, site_id: int, site_update: HistoricalSiteUpdate
) -> HistoricalSiteRead:
    updated_site = await da_update_historical_site(db, site_id, site_update)
    if updated_site:
        return HistoricalSiteRead.from_orm(updated_site)
    return None


async def delete_historical_site(db: AsyncSession, site_id: int) -> bool:
    return await da_delete_historical_site(db, site_id)
