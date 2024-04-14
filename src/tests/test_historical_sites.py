from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.data.database import get_session
from src.schemas.historical_site import HistoricalSiteCreate

client = TestClient(app)


def override_get_session():
    session = AsyncSession(bind=...)  # Create a test session
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session


def test_create_historical_site():
    test_site = HistoricalSiteCreate(
        name="Test Site",
        description="This is a test site",
        longitude=0.0,
        latitude=0.0,
        era="Test Era",
        tags=["test"],
        images=["test.jpg"],
    )
    response = client.post("/v1/historical-sites", json=test_site.model_dump())
    assert response.status_code == 201
    assert response.json()["name"] == "Test Site"
