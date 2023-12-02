from src.queries import users as user_queries
from src.hasher import Hasher
from src.models.users.models import User
from datetime import timedelta, datetime
from typing import TYPE_CHECKING
from config import app_config
from src.api.exceptions import users as user_exceptions
from jose import jwt, JWTError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def authenticate_user(
        email: str,
        password: str,
        session: 'AsyncSession',
) -> User | None:
    """Метод для проверки аутентификации пользователя по имейлу при логине."""
    user = await user_queries.get_user_by_email(
        email=email,
        session=session
    )
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


def create_token(
        data: dict,
        expires_delta: timedelta | None
):
    """Метод создания токена из data."""
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


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            app_config.secret,
            app_config.algorithm
        )
        email: str = payload.get("sub")
        if email is None:
            raise user_exceptions.WrongСredentials
    except JWTError:
        raise user_exceptions.WrongСredentials
    return email


async def get_user_by_decode_token(
        token: str,
        session: 'AsyncSession'
) -> User:
    """Получение пользователя путём декодирования токена с помощью email."""
    email = decode_token(token)
    user = await user_queries.get_user_by_email_with_checking_token(
        email=email,
        session=session,
        token=token
    )
    return user


async def get_user(token, session):
    """Получить пользователя."""
    user = await get_user_by_decode_token(token, session)
    if user is None:
        raise user_exceptions.UserNotFoundException
    return user


# async def check_user(token, session):
#     """Проверить, является ли пользователем."""
#     is_user = await get_user_by_decode_token(token, session)
#     if is_user is None:
#         return False
#     return True
