from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence, TYPE_CHECKING

from src.models.users.models import User, Follow

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_subscriptions(
    user_id: int,
    session: 'AsyncSession'
) -> Sequence[User]:
    query = (
        select(User).options(
            joinedload(User.following),
            joinedload(User.recipes)).where(
                Follow.following_id == user_id
            )
        )
    result = await session.scalars(query)
    return result.unique().all()
