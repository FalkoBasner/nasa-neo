from enum import StrEnum

from pydantic import BaseModel


class NeoFilter(StrEnum):
    hazardous = "hazardous"


class ValidationErrorResponse(BaseModel):
    detail: str


class NeoWeekResponse(BaseModel):
    week: int
    ids: list[str]


class UpstreamErrorDetail(BaseModel):
    code: int | None
    source: str
    message: str


class UpstreamErrorBody(BaseModel):
    code: int
    upstream: UpstreamErrorDetail


class ErrorResponse(BaseModel):
    error: UpstreamErrorBody


class ErrorSource(StrEnum):
    NASA = "nasa"


class UpstreamError(Exception):
    def __init__(self, detail: str, code: int | None, source: ErrorSource):
        self.detail = detail
        self.code = code
        self.source = source
