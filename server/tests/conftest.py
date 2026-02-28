from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.auth import create_token_for_user, get_password_hash
from src.core.database import Base, get_postgres_session
from src.main import app
from src.models.postgres.users import UserModel

# In-memory SQLite for tests
test_engine = create_async_engine("sqlite+aiosqlite://", echo=False)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_postgres_session] = override_get_session


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncIterator[None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user(db_session: AsyncSession) -> UserModel:
    user = UserModel(
        email="test@example.com",
        password_hash=get_password_hash("testpass123"),
        is_verified=True,
        is_superuser=False,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def superuser(db_session: AsyncSession) -> UserModel:
    user = UserModel(
        email="admin@example.com",
        password_hash=get_password_hash("adminpass123"),
        is_verified=True,
        is_superuser=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def auth_client(client: AsyncClient, test_user: UserModel) -> AsyncClient:
    token = create_token_for_user(test_user)
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture
async def superuser_client(client: AsyncClient, superuser: UserModel) -> AsyncClient:
    token = create_token_for_user(superuser)
    client.headers["Authorization"] = f"Bearer {token}"
    return client
