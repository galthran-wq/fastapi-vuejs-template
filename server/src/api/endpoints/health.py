from fastapi import APIRouter, Depends
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
async def readiness_check(session: AsyncSession = Depends(get_postgres_session)) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return {"status": "not_ready", "database": "disconnected"}
