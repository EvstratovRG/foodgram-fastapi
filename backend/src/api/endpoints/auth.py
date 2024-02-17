from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import app_config
from config.db import get_async_session
from src.api.constants.descriptions import auth as auth_descriptions
from src.api.constants.responses import auth as auth_responses
from src.api.constants.summaries import auth as auth_summaries
from src.api.dependencies.auth import get_current_user
from src.api.exceptions import users as user_exceptions
from src.auth.authorization import authenticate_user, create_token
from src.models.users import User
from src.queries.users import (add_token_to_user_instance,
                               delete_token_from_user_instance)
from src.schemas import base as base_schemas

router = APIRouter(prefix="/auth/token", tags=["/auth/token"])


@router.post(
    "/login/",
    status_code=status.HTTP_201_CREATED,
    summary=auth_summaries.getting_jwt_token,
    responses=auth_responses.post_token,
    response_model=base_schemas.Token,
    description=auth_descriptions.login_description,
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
        raise user_exceptions.WrongСredentials
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
        raise user_exceptions.WrongСredentials
    return {'auth_token': token}


@router.post(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=auth_summaries.del_jwt_token,
    response_description=auth_descriptions.logout_response_description,
    responses=auth_responses.delete_token,
    description=auth_descriptions.logout_description,
)
async def delete_users_token(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    deleted_token = await delete_token_from_user_instance(
        user=user,
        session=session,
    )
    if not deleted_token:
        raise user_exceptions.WrongСredentials
    return
