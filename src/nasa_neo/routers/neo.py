from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query

from nasa_neo.calendar import week_to_date_range
from nasa_neo.nasa_client import NasaClient, get_nasa_client

router = APIRouter()


@router.get("/neo/week/{week}")
async def get_neos_by_week(
    week: int,
    filter: str | None = Query(default=None),
    nasa_client: NasaClient = Depends(get_nasa_client),
):
    if week < 1 or week > 53:
        raise HTTPException(status_code=422, detail="Week must be between 1 and 53")

    year = date.today().year
    start, end = week_to_date_range(week, year)
    neos = await nasa_client.get_neos(start, end)

    if filter == "hazardous":
        neos = [n for n in neos if n["is_potentially_hazardous_asteroid"]]

    return {"week": week, "ids": [n["id"] for n in neos]}
