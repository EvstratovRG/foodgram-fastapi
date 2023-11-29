from src.queries import users as user_queries
from src.hasher import Hasher
from src.models.users.models import User
from datetime import timedelta, datetime
from config import get_app_config
from jose import jwt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def authenticate_user(
        email: str,
        password: str,
        session: 'AsyncSession',
) -> User | None:
    """Метод для проверки аутентификации пользователя по имейлу."""
    user = await user_queries.get_user_by_email(email=email, session=session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


def create_access_token(data: dict, expires_delta: timedelta | None):
    app_config = get_app_config()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=app_config.token_expire
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=app_config.secret,
        algorithm=app_config.algorithm
    )
    return encoded_jwt
