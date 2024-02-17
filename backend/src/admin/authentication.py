from datetime import timedelta
from typing import Self

from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select

from config import app_config
from config.db import AsyncSession
from src.auth.authorization import create_token, decode_admin_session_token
from src.hasher import Hasher
from src.models.users import User


class AdminAuth(AuthenticationBackend):
    async def login(
            self: Self,
            request: Request
            ) -> bool:
        form = await request.form()
        session = AsyncSession()
        email, password = form["username"], form["password"]
        # в поле username необходимо вносить email пользователя
        stmt = select(User).where(
            User.email == email
            ).where(
                User.is_superuser == bool(1)
            )
        try:
            user = await session.scalar(stmt)
            if user is None:
                return False
        finally:
            session.close()
        verify_is_admin = Hasher.verify_password(
            password,
            user.hashed_password
        )
        if verify_is_admin is not True:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=302,
            )
        token: str = create_token(
            data={'sub': user.email},
            expires_delta=timedelta(minutes=app_config.token_expire),
        )
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token: str = request.session.get('token')
        if not token:
            return False
        user_email = decode_admin_session_token(
            token.replace('Token ', ''),
            request,
        )
        if not user_email:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=302,
            )
        session = AsyncSession()
        stmt = select(User).where(User.email == user_email)
        try:
            user = await session.scalar(stmt)
        finally:
            await session.close()
        if user.is_superuser is True:
            return True
        return False
