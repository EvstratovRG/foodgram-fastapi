from fastapi import APIRouter, Depends, status
from typing import Any
from src.models.users.models import User
from src.queries import follows as follow_queries
from src.schemas import users as user_schemas
from src.schemas import base as base_schemas
from src.api.exceptions import users as user_exceptions
from src.api.endpoints.users import get_me
from config.db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["/users"])


@router.get(
    "/subscriptions",
    status_code=status.HTTP_200_OK,
    response_model=(
        list[user_schemas.GetSubscriptions] |
        base_schemas.ExceptionSchema
    )
)
async def gey_my_subscriptions(
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
