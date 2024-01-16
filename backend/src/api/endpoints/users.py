from fastapi import APIRouter, Depends, status, Query
from typing import Any
from src.models.users.models import User
from src.api.dependencies.auth import get_current_user
from src.api.exceptions import users as user_exceptions
from src.queries import users as user_queries
from src.schemas import users as user_schemas
from src.pagination import schemas as pagination_schema
from src.pagination.links import LinkCreator
from src.schemas import base as base_schemas
from src.hasher import Hasher
from config.db import get_async_session
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["/users"])
UserPagination = pagination_schema.Pagination[user_schemas.UserBaseSchema]


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserPagination
)
async def get_users(
    request: Request,
    page: int = Query(None),
    limit: int = Query(None),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """Получить список всех пользователей."""
    users = await user_queries.get_users(
        page=page,
        limit=limit,
        session=session
    )
    count = await user_queries.get_users_count(
        session=session
    )
    if users is None:
        raise user_exceptions.SomethingGoesWrong
    links = LinkCreator.generate_links(
        page=page,
        limit=limit,
        total=count,
        request=request
    )
    return UserPagination(
        count=count,
        result=users,
        **links
    )


@router.post(
    "/",
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


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserBaseSchema
)
async def get_me(
    user: User = Depends(get_current_user),
) -> Any:
    """Получить текущего пользователя."""
    return user


@router.post(
    "/set_password/",
    status_code=status.HTTP_200_OK,
    response_model=base_schemas.UpdatePasswordResponseSchema
)
async def change_users_password(
    user_schema: user_schemas.ChangeUserPassword,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """Изменить пароль текущего пользователя."""
    validate_current_password = Hasher.verify_password(
        user_schema.current_password,
        current_user.hashed_password
    )
    if not validate_current_password:
        raise user_exceptions.WrongPassword
    changed_password = await user_queries.update_password(
        session=session,
        user_id=current_user.id,
        current_password=Hasher.get_password_hash(
            user_schema.new_password
        )
    )
    if not changed_password:
        return status.HTTP_400_BAD_REQUEST
    return base_schemas.UpdatePasswordResponseSchema(
        status_code=status.HTTP_204_NO_CONTENT,
        detail='Пароль успешно изменен'
    )


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserBaseSchema
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Получить пользователя по id."""
    user = await user_queries.get_user(
        user_id=user_id,
        session=session
    )
    if user is None:
        raise user_exceptions.UserNotFoundException
    return user
