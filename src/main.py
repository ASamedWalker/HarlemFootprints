from fastapi import FastAPI
from contextlib import asynccontextmanager
from data.database import database, create_tables
from web.v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
