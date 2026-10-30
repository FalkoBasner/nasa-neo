from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

import nasa_neo.stats as stats
from nasa_neo.routers.error_handlers import register_error_handlers
from nasa_neo.routers.models import HealthResponse, RequestCounts, StatsResponse
from nasa_neo.routers.neo import router as neo_router

app = FastAPI()
app.include_router(neo_router)
register_error_handlers(app)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    path = request.url.path
    if path == "/health":
        stats.requests["health"] += 1
    elif path.startswith("/neo"):
        stats.requests["neo"] += 1
    elif path == "/stats":
        stats.requests["stats"] += 1
    return await call_next(request)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/stats", response_model=StatsResponse)
def get_stats() -> StatsResponse:
    counts = stats.requests
    return StatsResponse(requests=RequestCounts(total=sum(counts.values()), **counts))