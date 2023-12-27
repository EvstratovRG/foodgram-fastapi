from datetime import timedelta
from fastapi import APIRouter, Depends
from src.queries.users import (
    add_token_to_user_instance,
    delete_token_from_user_instance,
)
from src.auth.authorization import (
    authenticate_user,
    create_token,
)
from src.schemas import base as base_schemas
from config.db import get_async_session
from src.api.exceptions.users import SomethingGoesWrong, WrongСredentials
from config import app_config
from typing import Any
from src.api.dependencies.auth import get_current_user
from src.models.users.models import User

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth/token", tags=["/auth/token"])


@router.post(
    "/login/",
    response_model=base_schemas.Token
)
async def login_to_get_token(
    schema: base_schemas.AuthLoginSchema,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Получить токен авторизации."""
    user = await authenticate_user(
        email=schema.email,
        password=schema.password,
        session=session
    )
    if not user:
        raise WrongСredentials
    token = create_token(
        data={'sub': user.email},
        expires_delta=timedelta(minutes=app_config.token_expire),
    )
    added_token = await add_token_to_user_instance(
        user=user,
        login_token=token,
        session=session,
    )
    if not added_token:
        raise SomethingGoesWrong
    return {'token': token}


@router.post(
    "/logout/",
    response_model=base_schemas.StatusSchema
)
async def delete_users_token(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Удалить токен авторизации."""
    deleted_token = await delete_token_from_user_instance(
        user=user,
        session=session,
    )
    if not deleted_token:
        raise SomethingGoesWrong
    return {"status_code": 204,
            "is_deleted": deleted_token}
