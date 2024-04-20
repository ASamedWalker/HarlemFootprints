from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from data.database import get_session
from typing import Optional, List
from schemas.historical_site import (
    HistoricalSiteCreate,
    HistoricalSiteRead,
    HistoricalSiteUpdate,
)
from services.historical_site_service import (
    create_historical_site,
    get_historical_site,
    get_all_historical_sites,
    update_historical_site,
    delete_historical_site,
    search_historical_sites,
    search_nearby_sites,
    get_sites_by_date_range,
)
from models.historical_site import HistoricalSite


router = APIRouter()


@router.post("/", response_model=HistoricalSiteRead)
async def create_site_endpoint(
    site_create: HistoricalSiteCreate, db: AsyncSession = Depends(get_session)
):
    try:
        site = await create_historical_site(db, site_create)
        return site
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return site


@router.get("/search", response_model=list[HistoricalSite])
async def search_sites_endpoint(
    query: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    db: AsyncSession = Depends(get_session),
):
    try:
        sites = await search_historical_sites(db, query_string=query, tags=tags)
        return sites
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dates", response_model=list[HistoricalSiteRead])
async def fetch_sites_by_dates(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_session),
):
    sites = await get_sites_by_date_range(db, start_date, end_date)
    return sites


@router.get("/nearby", response_model=list[HistoricalSiteRead])
async def get_nearby_sites(
    latitude: float,
    longitude: float,
    max_distance: float,
    db: AsyncSession = Depends(get_session),
):
    try:
        sites = await search_nearby_sites(db, latitude, longitude, max_distance)
        return [HistoricalSiteRead.from_orm(site) for site in sites]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{site_id}", response_model=HistoricalSiteRead)
async def get_site_endpoint(site_id: int, db: AsyncSession = Depends(get_session)):
    site = await get_historical_site(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return HistoricalSiteRead.from_orm(site)


@router.get("/", response_model=list[HistoricalSiteRead])
async def get_all_sites_endpoint(db: AsyncSession = Depends(get_session)):
    try:
        sites = await get_all_historical_sites(db)
        return sites
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return HistoricalSiteRead.from_orm(sites)


@router.put("/{site_id}", response_model=HistoricalSiteRead)
async def update_site_endpoint(
    site_id: int,
    site_update: HistoricalSiteUpdate,
    db: AsyncSession = Depends(get_session),
):
    site = await update_historical_site(db, site_id, site_update)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return HistoricalSiteRead.from_orm(site)


@router.delete("/{site_id}", response_model=HistoricalSiteRead)
async def delete_site_endpoint(site_id: int, db: AsyncSession = Depends(get_session)):
    site = await delete_historical_site(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Not successful in deleting site")
    return HistoricalSiteRead.from_orm(site)
