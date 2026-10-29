from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from nasa_neo.errors import UpstreamError
from nasa_neo.routers.neo import router as neo_router

app = FastAPI()
app.include_router(neo_router)


@app.exception_handler(UpstreamError)
async def upstream_error_handler(_: Request, exc: UpstreamError):
    return JSONResponse(
        status_code=502,
        content={
            "error": {
                "status": 502,
                "upstream": {"code": exc.code, "source": exc.source, "message": exc.detail},
            },
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
