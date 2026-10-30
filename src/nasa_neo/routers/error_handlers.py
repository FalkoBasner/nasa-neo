from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from nasa_neo.routers.models import UpstreamError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError):
        first = exc.errors()[0]
        return JSONResponse(
            status_code=422,
            content={"detail": first["msg"]},
        )

    @app.exception_handler(UpstreamError)
    async def upstream_error_handler(_: Request, exc: UpstreamError):
        return JSONResponse(
            status_code=502,
            content={
                "error": {
                    "code": 502,
                    "upstream": {"code": exc.code, "source": exc.source, "message": exc.detail},
                },
            },
        )
