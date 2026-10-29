import os
import httpx
from datetime import date

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"


class NasaClient:
    async def get_neos(self, start: date, end: date) -> list[dict]:
        params = {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "api_key": NASA_API_KEY,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()  # raises httpx.HTTPStatusError on 4xx/5xx
            data = response.json()

        neos = []
        for day_neos in data["near_earth_objects"].values():
            neos.extend(day_neos)
        return neos


def get_nasa_client() -> NasaClient:
    return NasaClient()
