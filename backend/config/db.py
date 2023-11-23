from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings


async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=True,
)

sync_engine = create_engine(
    url=settings.database_url_psycopg,
    echo=True
)
# print(settings.database_url_psycopg, '\n\n\n\n\n\n\n\n\n\n')
AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)
SyncSession = sessionmaker(sync_engine)


def get_sync_session():
    db = SyncSession()
    try:
        yield db
    finally:
        db.close()


def get_async_session():
    db = AsyncSession()
    try:
        yield db
    finally:
        db.close()
