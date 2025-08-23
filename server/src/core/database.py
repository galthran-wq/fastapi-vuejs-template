import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

postgres_engine = create_async_engine(settings.postgres_url, echo=settings.debug)
AsyncSessionLocal = sessionmaker(
    postgres_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_postgres_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session