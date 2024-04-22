from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from api.historical_site_router import router as historical_site_router
from api.contributions_router import router as contributions_router
from data.database import create_tables
from pathlib import Path


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

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

origins = [
    "http://localhost:3000",  # React app address
    "http://localhost:8000",  # FastAPI server address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(historical_site_router, prefix="/sites", tags=["Historical Site"])
app.include_router(
    contributions_router, prefix="/contributions", tags=["Contributions"]
)
