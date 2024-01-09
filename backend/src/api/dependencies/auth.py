from fastapi import Request, Depends
from config.db import get_async_session, AsyncSession
from src.auth.authorization import (
    get_user,
)
from src.api.exceptions.users import WrongСredentials


async def get_current_user(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """Получаем текущего пользователя."""
    token = request.headers.get('Token')
    if not token:
        raise WrongСredentials
    user = await get_user(token, session)
    return user
