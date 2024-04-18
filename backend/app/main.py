from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.historical_site_router import router as historical_site_router
from data.database import create_tables


# Assuming you have a hypothetical function to load and unload resources
def load_resources():
    print("Loading resources...")
    # Code to load your resources, e.g. database connections, etc.


def unload_resources():
    print("Unloading resources...")
    # Code to unload/cleanup resources


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    load_resources()
    yield
    unload_resources()


app = FastAPI(lifespan=lifespan)


app.include_router(
    historical_site_router, prefix="/sites", tags=["Historical Site"]
)
