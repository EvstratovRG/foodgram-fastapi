from fastapi import APIRouter, Depends, status, Query, Request
from typing import Any
from src.pagination.links import LinkCreator
from src.pagination import schemas as pagination_schema
from src.models.users import User
from src.queries import subscriptions as subscribe_queries
from src.schemas import users as user_schemas
from src.api.exceptions import users as user_exceptions
from src.api.endpoints.users import get_me
from config.db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["/users"])
SubscibePagination = (
    pagination_schema.Pagination[user_schemas.GetSubscriptions]
)


@router.get(
    "/subscriptions/",
    status_code=status.HTTP_200_OK,
    response_model=SubscibePagination
)
async def get_my_subscriptions(
    request: Request,
    page: int = Query(None),
    limit: int = Query(None),
    recipes_limit: int = Query(None),
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    subscriptions = await subscribe_queries.get_subscriptions(
        page=page,
        limit=limit,
        user_id=current_user.id,
        session=session
    )
    count = await subscribe_queries.get_subscribed_users_count(
        user_id=current_user.id,
        session=session
    )
    if subscriptions is None:
        raise user_exceptions.SomethingGoesWrong
    subscriptions_schemas_list = []
    for follower in subscriptions:
        sub_schema = user_schemas.GetSubscriptions.model_validate(follower)
        sub_schema.recipes = (
            await subscribe_queries.get_subscribe_users_recipes(
                user_id=follower.id,
                recipes_limit=recipes_limit,
                session=session,
            )
        )
        sub_schema.recipes_count = (
            await subscribe_queries.get_subscribe_users_recipes_count(
                user_id=follower.id,
                session=session,
            )
        )
        subscriptions_schemas_list.append(sub_schema)
    links = LinkCreator.generate_links(
        page=page,
        limit=limit,
        total=count,
        request=request
    )
    return SubscibePagination(
        count=count,
        result=subscriptions_schemas_list,
        **links
    )


@router.post(
    "/{user_id}/subscribe/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schemas.GetSubscriptions
)
async def subscribe(
    user_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    subsribe = await subscribe_queries.subsribe(
        current_user_id=current_user.id,
        user_id=user_id,
        session=session
    )
    if subsribe is None:
        raise user_exceptions.SomethingGoesWrong
    return subsribe


@router.delete(
    "/{user_id}/subscribe/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsubscribe(
    user_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    subsribe = await subscribe_queries.unsubsribe(
        current_user_id=current_user.id,
        user_id=user_id,
        session=session
    )
    if not subsribe:
        raise user_exceptions.UserNotFoundException
    return None
