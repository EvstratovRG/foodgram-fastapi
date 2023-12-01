from fastapi import APIRouter, Depends, status
from typing import Any
from src.models.users.models import User
from src.api.dependencies.auth import get_current_user
from src.api.exceptions import users as user_exceptions
from src.queries import users as user_queries
from src.schemas import users as user_schemas
from src.schemas import base as base_schemas
from starlette.requests import Request
from src.hasher import Hasher

from config.db import get_async_session, AsyncSession


router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=(
        list[user_schemas.UserBaseSchema] |
        base_schemas.ExceptionSchema)
)
async def get_users(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
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


# @router.delete(
#     "",
#     status_code=status.HTTP_200_OK,
#     response_model=base_schemas.StatusSchema
# )
# async def delete_all_users(
#     session: AsyncSession = Depends(get_async_session),
# ) -> Any:
#     deleted_all_users = await user_queries.delete_all_users(
#         session=session
#     )
#     if not deleted_all_users:
#         return status.HTTP_400_BAD_REQUEST
#     return deleted_all_users


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserBaseSchema
)
async def get_me(
    user: User = Depends(get_current_user),
) -> Any:
    return user


@router.post(
    "/set_password",
    status_code=status.HTTP_200_OK,
    response_model=(
        base_schemas.UpdatePasswordResponseSchema |
        base_schemas.ExceptionSchema
    )
)
async def change_user_password(
    user_schema: user_schemas.ChangeUserPassword,
    user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    validate_current_password = Hasher.verify_password(
        user_schema.current_password,
        user.hashed_password
    )
    if not validate_current_password:
        raise user_exceptions.WrongСredentials('Пароль не соотвествует')
    changed_password = await user_queries.update_password(
        session=session,
        user_id=user.id,
        current_password=Hasher.get_password_hash(
            user_schema.current_password
        )
    )
    if not changed_password:
        return status.HTTP_400_BAD_REQUEST
    return base_schemas.UpdatePasswordResponseSchema(
        status_code=status.HTTP_204_NO_CONTENT,
        detail='Пароль успешно изменен'
    )


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

# @router.delete(
#     "/{user_id}",
#     status_code=status.HTTP_202_ACCEPTED,
#     response_model=base_schemas.StatusSchema
# )
# async def delete_user(
#     user_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ) -> Any:
#     deleted_user = await user_queries.delete_user(
#         session=session,
#         user_id=user_id
#     )
#     if not delete_user:
#         return status.HTTP_404_NOT_FOUND
#     return deleted_user
