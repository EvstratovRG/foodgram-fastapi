from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from backend.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


async_engine = create_async_engine(
    Settings.database_url_asyncpg,
    echo=True,
)

sync_engine = create_engine(
    Settings.database_url_psycopg,
    echo=True
)
# echo=True - в кансоль будут сыпаться запросы к бд
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
sync_session = sessionmaker(sync_engine)
