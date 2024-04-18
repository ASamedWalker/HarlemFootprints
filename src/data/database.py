import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from databases import Database
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
import logging

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        # Attempt to create tables
        await conn.run_sync(SQLModel.metadata.create_all)

        # Execute a raw SQL query to list tables for verification
        result = await conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        tables = await result.fetchall()
        print("Tables created:", [table[0] for table in tables])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
