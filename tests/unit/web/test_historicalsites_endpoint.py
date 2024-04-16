import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi.testclient import TestClient
from unittest.mock import patch, ANY, AsyncMock
from src.data.database import get_session

from src.main import app
from src.schemas.historical_site import HistoricalSiteUpdate
from src.models.historical_site import HistoricalSite
from src.services.historical_site_service import update_historical_site


# Fixture to manage the database state
@pytest.fixture(scope="module")
async def test_db():
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncTestingSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async def override_get_session():
        async with AsyncTestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def mock_session(mocker):
    mock = mocker.patch("src.data.database.get_session", autospec=True)
    session_mock = AsyncMock(spec=AsyncSession)
    mock.return_value = session_mock
    yield session_mock


@pytest.mark.asyncio
async def test_create_historical_site(test_db, mock_session):
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
    # Act: Send a request to the endpoint
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/historical-sites/", json=site_payload)

    # Assert: Check the response and any side-effects
    assert response.status_code == 201
    assert response.json()["name"] == "Historic Site One"
    # Add more assertions as needed

    # Verify interactions with the mock
    mock_session.commit.assert_called


@pytest.mark.asyncio
async def test_get_historical_site(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/historical-sites/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Historic Site One"
    assert response.json()["description"] == "Description of the historic site"


@pytest.mark.asyncio
async def test_get_all_historical_sites(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/historical-sites/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Historic Site One"
        assert response.json()[0]["description"] == "Description of the historic site"


@pytest.mark.asyncio
async def test_update_historical_site_success(mock_db_session):
    # Assuming we have a HistoricalSite model with fields that can be updated
    site_id = 1
    update_data = HistoricalSiteUpdate(
        name="Updated Name", description="Updated Description"
    )

    # Perform the update
    updated_site = await update_historical_site(mock_db_session, site_id, update_data)

    # Verify the site was updated correctly
    assert updated_site.name == "Updated Name"
    assert updated_site.description == "Updated Description"
    mock_db_session.commit.assert_called_once()
