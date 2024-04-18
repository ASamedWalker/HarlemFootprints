import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, ANY
from src.data.database import get_session, create_tables

from src.main import app

from src.schemas.historical_site import HistoricalSiteRead
import logging

logging.basicConfig(level=logging.DEBUG)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        # Log before creation
        existing_tables = await conn.run_sync(SQLModel.metadata.tables.keys)
        print("Existing tables before creation:", existing_tables)

        # Attempt to create tables
        await conn.run_sync(SQLModel.metadata.create_all)

        # Log after creation
        created_tables = await conn.run_sync(SQLModel.metadata.tables.keys)
        print("Tables after creation attempt:", created_tables)


@pytest.fixture(scope="module")
async def async_client():
    # Define the in-memory SQLite database URL
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"

    # Create an async engine specific for testing
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Define a session maker configured for async use
    AsyncTestingSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    # Function to override the get_session dependency
    def override_get_session():
        async def dependency_override():
            async with AsyncTestingSessionLocal() as session:
                yield session

        return dependency_override

    # Override the session dependency to provide a controlled session for tests
    app.dependency_overrides[get_session] = override_get_session

    # Ensure all tables are created
    await create_tables(engine)

    # Create an instance of AsyncClient bound to the FastAPI app
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        transport=ASGITransport(app=app, raise_app_exceptions=True),
    ) as client:
        yield client

    # Clear the dependency overrides after the tests are done
    app.dependency_overrides.clear()

    # Optionally, drop tables after tests if needed
    async with engine.begin() as conn:
        await conn.execute("DROP TABLE IF EXISTS historicalsite;")
        await conn.execute("DROP TABLE IF EXISTS other_related_tables_if_any;")


@pytest.fixture
async def mock_session(mocker):
    # Mock the session creation function
    mock = mocker.patch("src.data.database.get_session", autospec=True)
    session_mock = AsyncMock(spec=AsyncSession)
    mock.return_value = session_mock
    yield session_mock


# Assuming the use of a fixture 'async_client' that sets up AsyncClient correctly
@pytest.mark.asyncio
async def test_create_historical_site(async_client, mocker):
    site_payload = {
        "name": "Historic Site One",
        "description": "Description of the historic site",
        "longitude": -73.935242,
        "latitude": 40.730610,
        "address": "123 Test St",
        "era": "Modern",
        "tags": ["test", "historic"],
        "images": ["image1.jpg"],
        "audio_guide_url": "http://example.com/audio.mp3",
        "verified": True,
    }

    # Act: Send a request to the endpoint using the async_client
    response = await async_client.post("/v1/historical-sites/", json=site_payload)

    # Assert: Check the response status code and the content of the response
    assert (
        response.status_code == 201
    ), f"Expected 201 OK, got {response.status_code}. Response body: {response.text}"
    assert (
        response.json()["name"] == "Historic Site One"
    ), "Name in response does not match expected value"
    assert (
        response.json()["description"] == "Description of the historic site"
    ), "Description does not match expected value"


# @pytest.mark.asyncio
# async def test_get_historical_site(async_client):
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await async_client.get("/v1/historical-sites/1")
#         assert response.status_code == 200
#         assert response.json()["name"] == "Historic Site One"
#     assert response.json()["description"] == "Description of the historic site"


# @pytest.mark.asyncio
# async def test_get_all_historical_sites(async_client):
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await async_client.get("/v1/historical-sites/")
#         assert response.status_code == 200
#         assert len(response.json()) == 1
#         assert response.json()[0]["name"] == "Historic Site One"
#         assert response.json()[0]["description"] == "Description of the historic site"


# @pytest.mark.asyncio
# async def test_update_historical_site(async_client):
#     site_id = 1
#     update_payload = {
#         "name": "Updated Historic Site One",
#         "description": "Updated description of the historic site",
#         "longitude": -73.935242,
#         "latitude": 40.730610,
#         "address": "123 Test St",
#         "era": "Modern",
#         "tags": ["updated", "historic"],
#         "images": ["image2.jpg"],
#         "audio_guide_url": "http://example.com/new_audio.mp3",
#         "verified": True,
#     }

#     with patch(
#         "src.web.routes.historical_site_routes.update_historical_site_endpoint",
#         new_callable=AsyncMock,
#     ) as mock_update:
#         mock_update.return_value = HistoricalSiteRead(id=site_id, **update_payload)
#         response = await async_client.put(
#             f"/v1/historical-sites/{site_id}", json=update_payload
#         )
#         assert response.status_code == 200
#         assert response.json() == {"id": site_id, **update_payload}
#         mock_update.assert_called_once_with(ANY, site_id, ANY)


# @pytest.mark.asyncio
# async def test_update_historical_site_not_found(async_client, mocker):
#     site_id = 999  # Assuming this is the ID of a non-existent site
#     updated_site_data = {
#         "id": site_id,
#         "name": "Updated Historic Site One",
#         "description": "Updated description of the historic site",
#         "longitude": -73.935242,
#         "latitude": 40.730610,
#         "address": "123 Test St",
#         "era": "Modern",
#         "tags": ["updated", "historic"],
#         "images": ["image2.jpg"],
#         "audio_guide_url": "http://example.com/new_audio.mp3",
#         "verified": False,
#     }

#     # Mock the update function to return None, simulating not finding the site
#     mock_update_historical_site = mocker.patch(
#         "src.web.routes.historical_site_routes.update_historical_site_endpoint",
#         return_value=None,
#     )

#     # Perform the update via API call
#     response = await async_client.put(
#         f"/v1/historical-sites/{site_id}", json=updated_site_data
#     )

#     # Check the response status code and the error message
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Historical site not found"}
#     mock_update_historical_site.assert_called
