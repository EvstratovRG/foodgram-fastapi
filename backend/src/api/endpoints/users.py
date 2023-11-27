from fastapi import APIRouter, Depends, status
from typing import Any

from fastapi_pagination.links import Page
from fastapi_pagination import paginate
from backend.src.queries import users as user_queries
from backend.src.schemas import users as user_schemas
from backend.src.schemas import base as base_schemas
from backend.config.db import get_async_session, AsyncSession


router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Page[user_schemas.UserBaseSchema]:
    user = await user_queries.get_user(
        user_id=user_id,
        session=session
    )
    if user is None:
        return status.HTTP_404_NOT_FOUND
    return paginate(user_schemas.UserBaseSchema.model_validate(user))


# @router.get(
#     "/me",
#     status_code=status.HTTP_200_OK
# )
# async def get_current_user(
#     user_id: int,
#     session: AsyncSession = Depends(get_async_session)
# ) -> Any:
#     user = await user_queries.get_user(
#         user_id=user_id,
#         session=session
#     )
#     if user is None:
#         return status.HTTP_404_NOT_FOUND
#     return user_schemas.UserBaseSchema.model_validate(user)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_users(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    users = await user_queries.get_users(
        session=session
    )
    return [user_schemas.UserBaseSchema.model_validate(user) for user in users]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_schema: user_schemas.CreateUserSchema,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    created_user = await user_queries.create_user(
        session=session,
        user_schema=user_schema
    )
    return user_schemas.UserBaseSchema.model_validate(created_user)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK
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
    return user_schemas.UserBaseSchema.model_validate(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED
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
    return base_schemas.StatusSchema(success=deleted_user)
