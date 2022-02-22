import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data import config

Base = declarative_base()

engine = create_async_engine(
    config.DB_LINK,
    future=True
)

async_sessionmaker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
