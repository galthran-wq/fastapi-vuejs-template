from httpx import AsyncClient
from src.core.exceptions import AppError
from src.main import app


async def test_app_error_handler(client: AsyncClient) -> None:
    @app.get("/test-error")
    async def raise_error() -> None:
        raise AppError(status_code=418, detail="I'm a teapot")

    response = await client.get("/test-error")
    assert response.status_code == 418
    assert response.json() == {"detail": "I'm a teapot"}
