from fastapi import FastAPI
from contextlib import asynccontextmanager
from data.database import create_tables, get_session
from web.v1.router import router as v1_router


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

app.include_router(v1_router, prefix="/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
