from __future__ import annotations

from uuid import uuid4

from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from API.core.config import settings

from sqlalchemy.engine.url import URL


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"


def get_engine(url: URL | str = settings.database_url) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=False,
        pool_size=0,
        connect_args={
            "connection_class": CConnection,
        },
    )


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


db_url = settings.database_url
engine = get_engine(url=db_url)
sessionmaker = get_sessionmaker(engine)
