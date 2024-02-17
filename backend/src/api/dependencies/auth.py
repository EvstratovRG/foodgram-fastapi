from fastapi import Depends, Request

from config.db import AsyncSession, get_async_session
from src.api.exceptions.users import WrongСredentials
from src.auth.authorization import get_user


async def get_current_user(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """Получаем текущего пользователя."""
    token = request.headers.get('Authorization')
    if not token:
        raise WrongСredentials
    user = await get_user(token, session)
    return user
