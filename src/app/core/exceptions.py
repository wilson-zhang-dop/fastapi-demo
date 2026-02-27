"""Centralized exception handling and custom exception classes."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.logging import get_logger

logger = get_logger(__name__)


# ── Error response model ──────────────────────────────────────────────


class ErrorDetail(BaseModel):
    """Single error detail."""

    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    status_code: int
    error: str
    details: list[ErrorDetail] = []
    request_id: str | None = None


# ── Custom domain exceptions ──────────────────────────────────────────


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class EntityNotFoundError(AppException):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity: str, entity_id: Any) -> None:
        super().__init__(
            message=f"{entity} with id '{entity_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class EntityAlreadyExistsError(AppException):
    """Raised when creating a duplicate entity."""

    def __init__(self, entity: str, field: str, value: Any) -> None:
        super().__init__(
            message=f"{entity} with {field}='{value}' already exists",
            status_code=status.HTTP_409_CONFLICT,
        )


class BusinessRuleViolationError(AppException):
    """Raised when a domain business rule is violated."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


# ── Exception handlers ───────────────────────────────────────────────


def _build_error_response(
    status_code: int,
    error: str,
    details: list[ErrorDetail] | None = None,
) -> JSONResponse:
    body = ErrorResponse(
        status_code=status_code,
        error=error,
        details=details or [],
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


async def _app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    logger.warning("application_error", message=exc.message, status=exc.status_code)
    details = [ErrorDetail(**d) for d in exc.details]
    return _build_error_response(exc.status_code, exc.message, details)


async def _validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        ErrorDetail(field=" -> ".join(str(loc) for loc in e["loc"]), message=e["msg"])
        for e in exc.errors()
    ]
    return _build_error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Validation error",
        details,
    )


async def _unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception", error=str(exc))
    return _build_error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Internal server error",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the application."""
    app.add_exception_handler(AppException, _app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, _unhandled_exception_handler)
