from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import get_settings

settings = get_settings()


engine = create_async_engine(settings.database_url, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
