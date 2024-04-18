import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
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


async def create_tables():
    async with engine.begin() as conn:
        try:
            logger.info("Dropping existing tables...")
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.info("Creating new tables...")
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error(f"An error occurred when creating tables: {e}")



async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
