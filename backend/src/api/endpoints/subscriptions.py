from fastapi import APIRouter, Depends, status, Query, Request
from typing import Any
from src.models.recipes import Recipe
from src.pagination.links import LinkCreator
from src.models.users import User
from src.queries import subscriptions as subscribe_queries
from src.schemas import users as user_schemas
from src.schemas import recipes as recipe_schemas
from src.api.exceptions import users as user_exceptions
from src.api.endpoints.users import get_me
from src.api.constants.summaries import subscriptions as subscription_summaries
from config.db import get_async_session
from src.pagination import schemas as pagination_schemas
from src.api.constants.responses import subscriptions as subscription_responses
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "/subscriptions/",
    status_code=status.HTTP_200_OK,
    responses=subscription_responses.get_subscriptions,
    summary=subscription_summaries.get_current_user_subscriptions
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
    subscriptions_schemas_list: list[user_schemas.GetSubscriptions] = []
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
    return pagination_schemas.SubscibePagination(
        count=count,
        results=subscriptions_schemas_list,
        **links
    )


@router.post(
    "/{user_id}/subscribe/",
    status_code=status.HTTP_201_CREATED,
    responses=subscription_responses.create_subscribe,
    summary=subscription_summaries.subscribe_definite_user
)
async def subscribe(
    user_id: int,
    recipes_limit: int = Query(None),
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    subscriber = await subscribe_queries.subsribe(
        current_user_id=current_user.id,
        user_id=user_id,
        session=session
    )
    if subscriber is None:
        raise user_exceptions.SomethingGoesWrong
    subscriber_recipes: list[Recipe] = (
        await subscribe_queries.get_subscribe_users_recipes(
            user_id=subscriber.id,
            recipes_limit=recipes_limit,
            session=session,
        )
    )
    subscriber_recipes_count = (
        await subscribe_queries.get_subscribe_users_recipes_count(
            user_id=user_id,
            session=session,
        )
    )
    recipe_schema = [
        recipe_schemas.Subcriptions.model_validate(recipe)
        for recipe in subscriber_recipes
    ]
    response_schema = user_schemas.GetSubscriptions.model_validate(
        subscriber
    )
    response_schema.recipes = recipe_schema
    response_schema.recipes_count = subscriber_recipes_count
    return response_schema


@router.delete(
    "/{user_id}/subscribe/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=subscription_summaries.unsubscribe_user,
    responses=subscription_responses.delete_subscribe,
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
