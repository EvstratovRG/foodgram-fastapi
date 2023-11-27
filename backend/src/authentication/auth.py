from fastapi import Depends
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from config.db import AsyncSession, get_async_session
from src.models.users.models import User

from config import app_config


cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name="foodgram")

SECRET = app_config['secret']


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyBaseUserTable(session, User)
