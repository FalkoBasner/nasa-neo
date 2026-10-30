import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from nasa_neo.main import app
from nasa_neo.routers.models import UpstreamError
from nasa_neo.nasa_client import get_nasa_client

FIXTURE = json.loads(
    (Path(__file__).parent.parent / "http/nasa/nasa-feed-week-current.json").read_text()
)

ALL_IDS = {
    neo["id"]
    for neos in FIXTURE["near_earth_objects"].values()
    for neo in neos
}

HAZARDOUS_IDS = {
    neo["id"]
    for neos in FIXTURE["near_earth_objects"].values()
    for neo in neos
    if neo["is_potentially_hazardous_asteroid"]
}


def _flat_neos():
    neos = []
    for day_neos in FIXTURE["near_earth_objects"].values():
        neos.extend(day_neos)
    return neos


class FakeNasaClient:
    async def get_neos(self, start, end):
        return _flat_neos()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def override_nasa_client():
    # Replace the real NasaClient with FakeNasaClient for all tests in this module.
    # app.dependency_overrides is a dict keyed by the dependency function.
    app.dependency_overrides[get_nasa_client] = lambda: FakeNasaClient()
    yield
    app.dependency_overrides.clear()  # reset after each test


def test_week_returns_all_ids(client):
    response = client.get("/neo/week/44")
    assert response.status_code == 200
    body = response.json()
    assert body["week"] == 44
    assert set(body["ids"]) == ALL_IDS


def test_week_filter_hazardous(client):
    response = client.get("/neo/week/44?filter=hazardous")
    assert response.status_code == 200
    assert set(response.json()["ids"]) == HAZARDOUS_IDS


def test_week_invalid_low(client):
    response = client.get("/neo/week/0")
    assert response.status_code == 422


def test_week_invalid_high(client):
    response = client.get("/neo/week/54")
    assert response.status_code == 422


class RateLimitedNasaClient:
    async def get_neos(self, start, end):
        raise UpstreamError(detail="You have exceeded your rate limit.", code=429, source="nasa")


class UnreachableNasaClient:
    async def get_neos(self, start, end):
        raise UpstreamError(detail="NASA API unreachable", code=None, source="nasa")


def test_upstream_rate_limit_returns_502(client):
    app.dependency_overrides[get_nasa_client] = lambda: RateLimitedNasaClient()
    response = client.get("/neo/week/44")
    assert response.status_code == 502
    error = response.json()["error"]
    assert error["code"] == 502
    assert error["upstream"]["code"] == 429
    assert error["upstream"]["source"] == "nasa"
    assert error["upstream"]["message"] == "You have exceeded your rate limit."


def test_upstream_unreachable_returns_502(client):
    app.dependency_overrides[get_nasa_client] = lambda: UnreachableNasaClient()
    response = client.get("/neo/week/44")
    assert response.status_code == 502
    error = response.json()["error"]
    assert error["code"] == 502
    assert error["upstream"]["code"] is None
    assert error["upstream"]["message"] == "NASA API unreachable"
