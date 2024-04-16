from fastapi import APIRouter

from src.web.routes.historical_site_routes import router as historical_site_router

router = APIRouter()

router.include_router(historical_site_router, prefix="/historical-sites")