from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from config.db import AsyncSession
from src.models.users.models import User
from sqlalchemy import select
from src.hasher import Hasher
from typing import Self
from src.api.exceptions.users import WrongСredentials
from src.auth.authorization import create_token
from datetime import timedelta
from config import app_config
from src.auth.authorization import decode_token


class AdminAuth(AuthenticationBackend):
    async def login(
            self: Self,
            request: Request
            ) -> bool:
        form = await request.form()
        session = AsyncSession()
        email, password = form["username"], form["password"]
        stmt = select(User).where(
            User.email == email
            ).where(
                User.is_superuser == bool(1)
            )
        try:
            user = await session.scalar(stmt)
            if user is None:
                raise WrongСredentials
        finally:
            session.close()
        verify_is_admin = Hasher.verify_password(
            password,
            user.hashed_password
        )
        if verify_is_admin is not True:
            raise WrongСredentials
        token = create_token(
            data={'sub': user.email},
            expires_delta=timedelta(minutes=app_config.token_expire),
        )
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        user_email = decode_token(token)
        session = AsyncSession()
        stmt = select(User).where(User.email == user_email)
        try:
            user = await session.scalar(stmt)
        finally:
            session.close()
        if user.is_superuser is True:
            return True
        return False
