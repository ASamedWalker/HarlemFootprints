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
async def async_client():
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
    # Mock the session creation function
    mock = mocker.patch("src.data.database.get_session", autospec=True)
    session_mock = AsyncMock(spec=AsyncSession)
    mock.return_value = session_mock
    yield session_mock


@pytest.mark.asyncio
async def test_create_historical_site(async_client, mock_session):
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
        response = await async_client.post("/v1/historical-sites/", json=site_payload)

    # Assert: Check the response and any side-effects
    assert response.status_code == 201
    assert response.json()["name"] == "Historic Site One"
    # Add more assertions as needed

    # Verify interactions with the mock
    mock_session.commit.assert_called


@pytest.mark.asyncio
async def test_get_historical_site(async_client):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await async_client.get("/v1/historical-sites/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Historic Site One"
    assert response.json()["description"] == "Description of the historic site"


@pytest.mark.asyncio
async def test_get_all_historical_sites(async_client):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await async_client.get("/v1/historical-sites/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Historic Site One"
        assert response.json()[0]["description"] == "Description of the historic site"


@pytest.mark.asyncio
async def test_update_historical_site(async_client, mocker):
    site_id = 1
    original_site_data = {
        "id": site_id,
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
    updated_site_data = {
        "id": site_id,
        "name": "Updated Historic Site One",
        "description": "Updated description of the historic site",
        "longitude": -73.935242,  # Assuming no change
        "latitude": 40.730610,    # Assuming no change
        "address": "123 Test St",  # Assuming no change
        "era": "Modern",  # Assuming no change
        "tags": ["updated", "historic"],
        "images": ["image2.jpg"],
        "audio_guide_url": "http://example.com/new_audio.mp3",
        "verified": True,
    }

    # Mock the update function to return updated site data
    mock_update_historical_site = mocker.patch(
        "src.web.routes.historical_site_routes.update_historical_site_endpoint", return_value=updated_site_data
    )

    # Perform the update via API call
    response = await async_client.put(
        f"/v1/historical-sites/{site_id}", json=updated_site_data
    )

    # Check the response status code and data
    assert response.status_code == 200
    assert response.json() == updated_site_data
    mock_update_historical_site.assert_called_once_with(ANY, site_id, updated_site_data)


@pytest.mark.asyncio
async def test_update_historical_site_not_found(async_client, mocker):
    site_id = 1  # Assuming this is the ID of a non-existent site
    updated_site_data = {
        "id": site_id,
        "name": "Updated Historic Site One",
        "description": "Updated description of the historic site",
        "longitude": -73.935242,
        "latitude": 40.730610,
        "address": "123 Test St",
        "era": "Modern",
        "tags": ["updated", "historic"],
        "images": ["image2.jpg"],
        "audio_guide_url": "http://example.com/new_audio.mp3",
        "verified": True,
    }

    # Mock the update function to return None, simulating not finding the site
    mock_update_historical_site = mocker.patch(
        "src.web.routes.historical_site_routes.update_historical_site_endpoint", return_value=None
    )

    # Perform the update via API call
    response = await async_client.put(
        f"/v1/historical-sites/{site_id}", json=updated_site_data
    )

    # Check the response status code and the error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
    mock_update_historical_site.assert_called
