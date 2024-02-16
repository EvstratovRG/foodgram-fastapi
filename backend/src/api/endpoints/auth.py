from datetime import timedelta
from fastapi import APIRouter, Depends, status
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
from src.models.users import User
from src.api.constants.summaries import auth as auth_summaries

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth/token", tags=["/auth/token"])


@router.post(
    "/login/",
    response_model=base_schemas.Token,
    status_code=status.HTTP_201_CREATED,
    summary=auth_summaries.getting_jwt_token,
)
async def login_to_get_token(
    schema: base_schemas.AuthLoginSchema,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
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
        login_token=token.replace("Token ", ""),
        session=session,
    )
    if not added_token:
        raise SomethingGoesWrong
    return {'auth_token': token}


@router.post(
    "/logout/",
    response_model=base_schemas.StatusSchema,
    summary=auth_summaries.del_jwt_token
)
async def delete_users_token(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    deleted_token = await delete_token_from_user_instance(
        user=user,
        session=session,
    )
    if not deleted_token:
        raise SomethingGoesWrong
    return {"status_code": 204,
            "is_deleted": deleted_token}
