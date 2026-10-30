import os
from datetime import date

import httpx

from nasa_neo.routers.models import ErrorSource, UpstreamError

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"


class NasaClient:
    async def get_neos(self, start: date, end: date) -> list[dict]:
        params = {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "api_key": NASA_API_KEY,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(BASE_URL, params=params)
                response.raise_for_status()  # raises httpx.HTTPStatusError on 4xx/5xx
                data = response.json()
        except httpx.HTTPStatusError as e:
            try:
                nasa_message = e.response.json().get("error", {}).get("message")
            except Exception:
                nasa_message = None
            raise UpstreamError(
                detail=nasa_message or "NASA API error",
                code=e.response.status_code,
                source=ErrorSource.NASA,
            )
        except httpx.RequestError:
            # network-level failure: DNS, connection refused, timeout
            raise UpstreamError(
                detail="NASA API unreachable",
                code=None,
                source=ErrorSource.NASA,
            )

        neos = []
        for day_neos in data["near_earth_objects"].values():
            neos.extend(day_neos)
        return neos


def get_nasa_client() -> NasaClient:
    return NasaClient()
