from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

database = Database(DATABASE_URL)


async def create_tables():
    async with engine.begin() as conn:
        try:
            # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
        except Exception as e:
            print(f"An error occurred when creating the tables: {e}")


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
