import json
from datetime import date
from pathlib import Path

import httpx
import pytest
import respx

from nasa_neo.routers.models import UpstreamError
from nasa_neo.nasa_client import NasaClient

FIXTURE = json.loads(
    (Path(__file__).parent.parent / "http/nasa/nasa-feed-week-current.json").read_text()
)

EXPECTED_IDS = {
    neo["id"]
    for neos in FIXTURE["near_earth_objects"].values()
    for neo in neos
}

NASA_FEED_URL = "https://api.nasa.gov/neo/rest/v1/feed"


@pytest.mark.anyio
@respx.mock
async def test_get_neos_flattens_all_days():
    respx.get(NASA_FEED_URL).mock(return_value=httpx.Response(200, json=FIXTURE))

    result = await NasaClient().get_neos(date(2026, 10, 27), date(2026, 11, 2))

    assert {neo["id"] for neo in result} == EXPECTED_IDS


@pytest.mark.anyio
@respx.mock
async def test_get_neos_passes_correct_params():
    route = respx.get(NASA_FEED_URL).mock(return_value=httpx.Response(200, json=FIXTURE))

    await NasaClient().get_neos(date(2026, 10, 27), date(2026, 11, 2))

    assert route.called
    assert route.calls.last.request.url.params["start_date"] == "2026-10-27"
    assert route.calls.last.request.url.params["end_date"] == "2026-11-02"
    assert route.calls.last.request.url.params["api_key"] == "DEMO_KEY"


@pytest.mark.anyio
@respx.mock
async def test_rate_limit_raises_upstream_error_with_nasa_message():
    respx.get(NASA_FEED_URL).mock(return_value=httpx.Response(
        429, json={"error": {"code": "OVER_RATE_LIMIT", "message": "You have exceeded your rate limit."}}
    ))

    with pytest.raises(UpstreamError) as exc_info:
        await NasaClient().get_neos(date(2026, 10, 27), date(2026, 11, 2))

    assert exc_info.value.code == 429
    assert exc_info.value.source == "nasa"
    assert exc_info.value.detail == "You have exceeded your rate limit."


@pytest.mark.anyio
@respx.mock
async def test_http_error_without_body_falls_back_to_default_message():
    respx.get(NASA_FEED_URL).mock(return_value=httpx.Response(500))

    with pytest.raises(UpstreamError) as exc_info:
        await NasaClient().get_neos(date(2026, 10, 27), date(2026, 11, 2))

    assert exc_info.value.code == 500
    assert exc_info.value.detail == "NASA API error"


@pytest.mark.anyio
@respx.mock
async def test_network_error_raises_upstream_error():
    respx.get(NASA_FEED_URL).mock(side_effect=httpx.ConnectError("connection refused"))

    with pytest.raises(UpstreamError) as exc_info:
        await NasaClient().get_neos(date(2026, 10, 27), date(2026, 11, 2))

    assert exc_info.value.code is None
    assert exc_info.value.detail == "NASA API unreachable"
