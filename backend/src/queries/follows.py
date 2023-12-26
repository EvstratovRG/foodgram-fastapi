from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from typing import Sequence, TYPE_CHECKING
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status
from src.queries import users as user_queries
from src.models.users.models import User, Follow
from sqlalchemy.exc import SQLAlchemyError
from src.api.exceptions import users as user_exceptions

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


async def subsribe(
    user_id: int,
    current_user_id: int,
    session: 'AsyncSession'
) -> User | None:
    if user_id == current_user_id:
        raise user_exceptions.BadSubscribe
    stmt = insert(Follow).values(
        follower_id=user_id,
        following_id=current_user_id
    )
    try:
        follow = await session.scalars(stmt)
        if not follow:
            raise IntegrityError('Пользователь не создан')
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    await session.commit()
    follower = await user_queries.get_user(session, user_id)
    return follower


async def unsubsribe(
    user_id: int,
    current_user_id: int,
    session: 'AsyncSession'
) -> bool:
    follow = select(Follow).where(
        Follow.follower_id == user_id,
        Follow.following_id == current_user_id
    )
    result = await session.scalars(follow)
    if follow is None:
        return False
    try:
        await session.delete(result.first())
        await session.commit()
    except SQLAlchemyError:
        return False
    return True
