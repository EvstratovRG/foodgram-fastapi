from fastapi import APIRouter, Depends, status
from typing import Any
from src.models.users import User
from src.queries import follows as follow_queries
from src.schemas import users as user_schemas
from src.api.exceptions import users as user_exceptions
from src.api.endpoints.users import get_me
from config.db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "/subscriptions/",
    status_code=status.HTTP_200_OK,
    response_model=list[user_schemas.GetSubscriptions]
)
async def get_my_subscriptions(
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    subscriptions = await follow_queries.get_subscriptions(
        user_id=current_user.id,
        session=session
    )
    if subscriptions is None:
        raise user_exceptions.SomethingGoesWrong
    return subscriptions


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
    subsribe = await follow_queries.subsribe(
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
    subsribe = await follow_queries.unsubsribe(
        current_user_id=current_user.id,
        user_id=user_id,
        session=session
    )
    if not subsribe:
        raise user_exceptions.UserNotFoundException
    return None
