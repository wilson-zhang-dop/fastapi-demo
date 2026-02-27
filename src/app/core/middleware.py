"""Application middleware."""

import time
import uuid

from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


async def logging_middleware(request: Request, call_next) -> Response:  # noqa: ANN001
    """Log every request/response with timing and a unique request id."""
    request_id = str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start = time.perf_counter()
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None,
    )

    response: Response = await call_next(request)

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "request_finished",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        elapsed_ms=elapsed_ms,
    )

    response.headers["X-Request-ID"] = request_id
    return response


def register_middleware(app: FastAPI) -> None:
    """Register all middleware on the application."""
    app.middleware("http")(logging_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
