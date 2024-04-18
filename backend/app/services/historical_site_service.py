from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.sql import or_
from sqlalchemy import func
from geoalchemy2 import Geography
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from typing import List, Optional
import logging


from models.historical_site import HistoricalSite
from schemas.historical_site import HistoricalSiteCreate, HistoricalSiteUpdate


from schemas.historical_site import (
    HistoricalSiteCreate,
    HistoricalSiteUpdate,
)

logger = logging.getLogger(__name__)


async def create_historical_site(
    db: AsyncSession, site_create: HistoricalSiteCreate
) -> HistoricalSite:
    try:
        site = HistoricalSite(**site_create.dict())
        db.add(site)
        logger.info(f"Creating historical site: {site_create.name}")
        await db.commit()
        logger.info(f"Successfully created historical site: {site_create.name}")
        await db.refresh(site)
        logger.info(f"Refreshing historical site: {site_create.name}")
        return site
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Historical site already exists")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_historical_site(db: AsyncSession, site_id: int) -> HistoricalSite:
    try:
        stmt = select(HistoricalSite).where(HistoricalSite.id == site_id)
        result = await db.execute(stmt)
        site = result.scalars().first()
        if site is None:
            raise HTTPException(status_code=404, detail="Historical site not found")
        return site
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Historical site not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_historical_sites(db: AsyncSession) -> List[HistoricalSite]:
    try:
        stmt = select(HistoricalSite)
        result = await db.execute(stmt)
        sites = result.scalars().all()
        return sites
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_historical_site(
    db: AsyncSession, site_id: int, site_update: HistoricalSiteUpdate
) -> HistoricalSite:
    try:
        stmt = select(HistoricalSite).where(HistoricalSite.id == site_id)
        result = await db.execute(stmt)
        site = result.scalars().first()
        if site is None:
            raise HTTPException(status_code=404, detail="Historical site not found")
        for field, value in site_update.dict(exclude_unset=True).items():
            setattr(site, field, value)
        db.add(site)
        await db.commit()
        await db.refresh(site)
        return site
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Historical site not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_historical_site(db: AsyncSession, site_id: int) -> bool:
    try:
        stmt = select(HistoricalSite).where(HistoricalSite.id == site_id)
        result = await db.execute(stmt)
        site = result.scalars().first()
        if site is None:
            raise HTTPException(status_code=404, detail="Historical site not found")
        db.delete(site)
        await db.commit()
        return True
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Historical site not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def search_historical_sites(
    db: AsyncSession,
    query_string: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> List[HistoricalSite]:
    try:
        query = select(HistoricalSite)
        if query_string:
            query = query.filter(
                or_(
                    HistoricalSite.name.ilike(f"%{query_string}%"),
                    HistoricalSite.description.ilike(f"%{query_string}%"),
                )
            )

        if tags:
            query = query.filter(HistoricalSite.tags.any(tag.in_(tags)))

        result = await db.execute(query)
        sites = result.scalars().all()
        return sites

        if tags:
            query = query.filter(HistoricalSite.tags.any(tag.in_(tags)))

        result = await db.execute(query)
        sites = result.scalars().all()
        return sites
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def search_nearby_sites(
    db: AsyncSession, latitude: float, longitude: float, radius: float
) -> List[HistoricalSite]:
    try:
        # Convert latitude and longitude to a Point geography type directly in the query
        point = func.ST_Point(longitude, latitude, type_=Geography)
        stmt = select(HistoricalSite).where(
            func.ST_DWithin(HistoricalSite.location, point, radius)
        )
        result = await db.execute(stmt)
        sites = result.scalars().all()
        return sites
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))