import nasa_neo.stats as stats
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def setup_function():
    stats.request_count = 0


def test_stats_counts_requests():
    client.get("/health")
    client.get("/health")
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["requests"] == 3


def test_stats_counts_across_endpoints():
    client.get("/health")
    client.get("/stats")
    response = client.get("/stats")
    assert response.json()["requests"] == 3
