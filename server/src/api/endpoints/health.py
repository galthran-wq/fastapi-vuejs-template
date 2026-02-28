from fastapi import APIRouter
from src.schemas.health import HealthResponse

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "API is running"}


@router.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
