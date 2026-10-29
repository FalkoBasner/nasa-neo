from enum import StrEnum


class ErrorSource(StrEnum):
    NASA = "nasa"


class UpstreamError(Exception):
    def __init__(self, detail: str, code: int | None, source: ErrorSource):
        self.detail = detail
        self.code = code
        self.source = source
