import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
from unittest.mock import patch, ANY

from main import app
from schemas.historical_site import HistoricalSiteUpdate


# Fixture to manage the database state
@pytest.fixture(scope="function")
async def test_db():
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create a session for the test
    async with AsyncSessionLocal() as session:
        yield session

    # Drop all tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


client = TestClient(app)

site_data = {
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


@pytest.fixture
def mock_create_site():
    with patch(
        "services.historical_site_service.create_historical_site",
        return_value={"id": 1, **site_data},
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_all_sites(test_db):
    with patch(
        "services.historical_site_service.get_all_historical_sites",
        return_value=[{"id": 1, **site_data}],
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_site(test_db):
    with patch(
        "services.historical_site_service.get_historical_site",
        return_value={"id": 1, **site_data},
    ) as mock:
        yield mock


@pytest.fixture
def mock_update_site(test_db):
    with patch(
        "services.historical_site_service.update_historical_site",
        return_value={"id": 1, **site_data},
    ) as mock:
        yield mock


def test_create_historical_site(mock_create_site):
    response = client.post("/v1/historical-sites/", json=site_data)
    assert response.status_code == 201
    assert response.json()["name"] == site_data["name"]
    # mock_create_site.assert_called_once()


def test_get_all_historical_sites(mock_get_all_sites):
    # Assume we post a new site in the setup or as part of the test if not done elsewhere.
    site_data = {
        "name": "Unique Historic Site",
        "description": "Unique Description",
        "longitude": -73.935242,
        "latitude": 40.730610,
        "address": "Unique Address",
        "era": "Modern",
        "tags": ["unique", "test"],
        "images": ["uniqueimage.jpg"],
        "audio_guide_url": "http://example.com/uniqueaudio.mp3",
        "verified": True,
    }
    client.post("/v1/historical-sites/", json=site_data)

    # Now, retrieve all sites and check for the presence of this unique site
    response = client.get("/v1/historical-sites/")
    assert response.status_code == 200
    sites = response.json()
    # Check that our unique site is in the list of all sites returned
    assert any(
        site["name"] == "Unique Historic Site" for site in sites
    ), "Unique site not found in response"


def test_get_historical_site(mock_get_site):
    response = client.get("/v1/historical-sites/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Historic Site One"


def test_update_historical_site(mock_update_site):
    # Setup the update data
    local_site_data = {
        "name": "Test Site Original",
        "description": "Original description of the site",
        "longitude": -73.935242,
        "latitude": 40.730610,
        "address": "123 Test Address",
        "era": "Contemporary",
        "tags": ["original", "test"],
        "images": ["original.jpg"],
        "audio_guide_url": "http://example.com/original.mp3",
        "verified": True,
    }

    update_data = {
        "name": "Updated Test Site",
        "description": "Updated description of the site",
    }

    expected_response_data = {**local_site_data, **update_data, "id": 1}
    mock_update_site.return_value = expected_response_data

    # Execute the PUT request to update the historical site
    response = client.put("/v1/historical-sites/1", json=update_data)

    # Verify the response from the update
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Updated Test Site"
    assert response_data["description"] == "Updated description of the site"

    # # # Verify that the mock was indeed called
    # mock_update_site.assert_called_once_with(ANY, 1, ANY)
