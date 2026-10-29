from fastapi import FastAPI, Request

import nasa_neo.stats as stats
from nasa_neo.routers.error_handlers import register_error_handlers
from nasa_neo.routers.neo import router as neo_router

app = FastAPI()
app.include_router(neo_router)
register_error_handlers(app)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    stats.request_count += 1
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def get_stats():
    return {"requests": stats.request_count}
