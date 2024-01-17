from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_db_config

db_config = get_db_config()
async_engine = create_async_engine(
    url=db_config.database_url_asyncpg,
    # echo=True,
)
sync_engine = create_engine(
    url=db_config.database_url_psycopg,
    # echo=True
)
AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)
SyncSession = sessionmaker(sync_engine)


def get_sync_session():
    """Устанавливаем синхронную сесситю с базой данных."""
    db = SyncSession()
    try:
        yield db
    finally:
        db.close()


async def get_async_session():
    """Устанавливаем асинхронную сессию с базой данных."""
    db = AsyncSession()
    try:
        yield db
    finally:
        await db.close()
