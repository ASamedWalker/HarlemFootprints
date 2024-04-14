from fastapi import FastAPI
from contextlib import asynccontextmanager
from .data.database import database, create_tables
from .web.v1.endpoints import router

app = FastAPI()


app.include_router(router, prefix="/v1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
