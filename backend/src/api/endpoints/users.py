from fastapi import APIRouter, Depends, status, Query
from typing import Any
from src.models.users import User
from src.api.dependencies.auth import get_current_user
from src.api.exceptions import users as user_exceptions
from src.queries import users as user_queries
from src.schemas import users as user_schemas
from src.pagination import schemas as pagination_schema
from src.pagination.links import LinkCreator
from src.hasher import Hasher
from config.db import get_async_session
from fastapi import Request
from src.api.constants.summaries import users as user_summaries
from src.api.constants.responses import users as user_responses
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=user_responses.get_users,
    summary=user_summaries.get_the_list_of_users
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
    return pagination_schema.UserPagination(
        count=count,
        results=users,
        **links
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description='Регистрация пользователя',
    responses=user_responses.create_user,
    summary=user_summaries.create_user_form
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
        raise user_exceptions.AlreadyExists
    return user_schemas.UserBaseSchema.model_validate(create_user)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    responses=user_responses.get_me,
    summary=user_summaries.get_current_user
)
async def get_me(
    user: User = Depends(get_current_user),
) -> Any:
    """Получить текущего пользователя."""
    return user_schemas.UserBaseSchema.model_validate(user)


@router.post(
    "/set_password/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=user_summaries.change_password_of_current_user,
    response_description='Пароль успешно изменен.',
    responses=user_responses.set_password
)
async def change_users_password(
    user_schema: user_schemas.ChangeUserPassword,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session),
):
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
        raise user_exceptions.ChangePassword
    return


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    responses=user_responses.get_user,
    summary=user_summaries.get_user_by_id,
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
        raise user_exceptions.UserNotFound
    return user_schemas.UserBaseSchema.model_validate(user)
