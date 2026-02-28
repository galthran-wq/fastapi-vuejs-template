from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


postgres_engine = create_async_engine(settings.postgres_url, echo=settings.debug)
AsyncSessionLocal = sessionmaker(postgres_engine, class_=AsyncSession, expire_on_commit=False)


async def get_postgres_session() -> AsyncSession:  # type: ignore[misc]
    async with AsyncSessionLocal() as session:
        yield session
