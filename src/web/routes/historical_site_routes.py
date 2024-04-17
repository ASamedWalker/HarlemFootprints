from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.historical_site_service import (
    create_historical_site,
    get_historical_site,
    get_all_historical_sites,
    update_historical_site,
    delete_historical_site,
)
from src.schemas.historical_site import (
    HistoricalSiteCreate,
    HistoricalSiteRead,
    HistoricalSiteUpdate,
)
from src.data.database import get_session


router = APIRouter()


@router.post(
    "/",
    response_model=HistoricalSiteRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_site(
    site: HistoricalSiteCreate, db: AsyncSession = Depends(get_session)
):
    return await create_historical_site(db, site)


@router.get("/{site_id}", response_model=HistoricalSiteRead)
async def read_site(site_id: int, db: AsyncSession = Depends(get_session)):
    site = await get_historical_site(db, site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.get("/", response_model=List[HistoricalSiteRead])
async def read_sites(db: AsyncSession = Depends(get_session)):
    return await get_all_historical_sites(db)


@router.put("/{site_id}", response_model=HistoricalSiteRead)
async def update_historical_site_endpoint(
    site_id: int,
    site_update: HistoricalSiteUpdate,
    session: AsyncSession = Depends(get_session),
) -> HistoricalSiteUpdate:
    # Convert Pydantic model to dictionary for updating model fields
    site_update_dict = site_update.model_dump(exclude_unset=True)

    updated_historical_site = await update_historical_site(
        session, site_id, site_update_dict
    )
    if not updated_historical_site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Historical site not found"
        )
    return updated_historical_site


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(site_id: int, db: AsyncSession = Depends(get_session)):
    success = await delete_historical_site(db, site_id)
    if not success:
        raise HTTPException(status_code=404, detail="Site not found")
