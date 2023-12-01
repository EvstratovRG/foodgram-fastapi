from fastapi import Request, Depends
from config.db import get_async_session, AsyncSession
from src.auth.authorization import (
    get_user_by_decode_token,
    check_is_user_by_decode_token
)


async def get_current_user(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    token = request.headers.get('Token')
    user = await get_user_by_decode_token(token, session)
    return user


async def check_user_with_token(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    token = request.headers.get('Token')
    is_user: bool = await check_is_user_by_decode_token(token, session)
    return is_user
