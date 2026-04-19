from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class DomainError(Exception):
    status_code = 400
    code = "DOMAIN_ERROR"

    def __init__(self, message: str, details: Any = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundError(DomainError):
    status_code = 404
    code = "NOT_FOUND"


class BadRequestError(DomainError):
    status_code = 400
    code = "BAD_REQUEST"


class ScheduleConflictError(DomainError):
    status_code = 409
    code = "SCHEDULE_CONFLICT"


def _payload(exc: DomainError) -> dict[str, Any]:
    payload = {"code": exc.code, "message": exc.message}
    if exc.details is not None:
        payload["details"] = exc.details
    return payload


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=_payload(exc))
