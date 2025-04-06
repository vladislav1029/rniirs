from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)


from src.config import settings
from src.repository.models import Base


async_engine = create_async_engine(url=settings.URL, echo=True)

async_session = async_sessionmaker(async_engine)


async def create_table():

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
