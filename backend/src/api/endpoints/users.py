from fastapi import APIRouter, Depends, status
from typing import Any
from src.api.endpoints.auth import login_to_get_token
from src.api.exceptions import users as user_exceptions
from src.queries import users as user_queries
from src.schemas import users as user_schemas
from src.schemas import base as base_schemas
from jose import jwt, JWTError
from config import app_config

from config.db import get_async_session, AsyncSession


router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserBaseSchema
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    user = await user_queries.get_user(
        user_id=user_id,
        session=session
    )
    if user is None:
        raise user_exceptions.UserNotFoundException
    return user


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserBaseSchema
)
async def get_current_user(
    token: str = Depends(login_to_get_token),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    try:
        payload = jwt.decode(
            token,
            app_config.secret,
            app_config.algorithm
        )
        email = payload.get("sub")
        if email is None:
            raise user_exceptions.WrongСredentials
    except JWTError:
        raise user_exceptions.WrongСredentials
    user = await user_queries.get_user(
        email=email,
        session=session
    )
    if user is None:
        raise user_exceptions.UserNotFoundException
    return user


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[user_schemas.UserBaseSchema]
)
async def get_users(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    users = await user_queries.get_users(
        session=session
    )
    if users is None:
        raise user_exceptions.SomethingGoesWrong
    return users


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description='Регистрация пользователя',
    response_model=user_schemas.UserBaseSchema
)
async def create_user(
    user_schema: user_schemas.CreateUserSchema,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Регистрация пользователя."""
    created_user = await user_queries.create_user(
        session=session,
        user_schema=user_schema
    )
    if created_user is None:
        raise user_exceptions.AlreadyExistsException
    return created_user


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserBaseSchema
)
async def update_user(
    user_id: int,
    user_schema: user_schemas.CreateUserSchema,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    updated_user = await user_queries.update_user(
        session=session,
        user_id=user_id,
        user_schema=user_schema
    )
    if not update_user:
        return status.HTTP_404_NOT_FOUND
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=base_schemas.StatusSchema
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    deleted_user = await user_queries.delete_user(
        session=session,
        user_id=user_id
    )
    if not delete_user:
        return status.HTTP_404_NOT_FOUND
    return deleted_user


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=base_schemas.StatusSchema
)
async def delete_all_users(
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    deleted_all_users = await user_queries.delete_all_users(
        session=session
    )
    if not deleted_all_users:
        return status.HTTP_400_BAD_REQUEST
    return deleted_all_users
