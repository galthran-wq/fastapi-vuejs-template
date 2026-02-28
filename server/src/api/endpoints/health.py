from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_postgres_session
from src.schemas.health import HealthResponse

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "API is running"}


@router.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")


@router.get("/ready")
async def readiness_check(
    session: AsyncSession = Depends(get_postgres_session),
) -> dict[str, str] | JSONResponse:
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "database": "disconnected"},
        )
