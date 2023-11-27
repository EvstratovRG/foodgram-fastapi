from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import db_config


async_engine = create_async_engine(
    url=db_config.database_url_asyncpg,
    echo=True,
)

sync_engine = create_engine(
    url=db_config.database_url_psycopg,
    echo=True
)
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
