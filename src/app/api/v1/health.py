"""Health, readiness, and liveness endpoints."""

from fastapi import APIRouter, status
from sqlalchemy import text

from app.db.session import engine

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """Basic liveness probe — always returns OK if the process is running."""
    return {"status": "ok"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> dict[str, str]:
    """Readiness probe — verifies the database connection is working."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}
