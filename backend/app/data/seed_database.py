from sqlmodel import SQLModel
from sqlalchemy import text
from data.database import AsyncSessionLocal, create_tables
from models.historical_site import HistoricalSite
from data.seed_data import historical_sites


async def seed_historical_sites():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Check if data already exists to avoid duplicates
            existing_count = await session.execute(
                text("SELECT COUNT(*) FROM historicalsite")
            )
            if existing_count.scalars().first() > 0:
                return "Data already seeded!"

            for site in historical_sites:
                new_site = HistoricalSite(**site)
                session.add(new_site)

            # Commit once after all inserts are done
            await session.commit()
    return "Data seeded successfully!"


async def main():
    try:
        print("Creating tables...")
        await create_tables()
        print("Tables created!")

        print("Seeding data...")
        message = await seed_historical_sites()
        print(message)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
