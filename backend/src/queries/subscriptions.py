from typing import TYPE_CHECKING, Sequence

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import func, insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.api.exceptions import users as user_exceptions
from src.models.recipes import Follow, Recipe
from src.models.users import User
from src.pagination.paginate import paginate
from src.queries import users as user_queries

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_subscriptions(
    page: int,
    limit: int,
    user_id: int,
    session: 'AsyncSession'
) -> Sequence[User]:
    stmt = (
        select(User).options(
            joinedload(User.follower)).where(
                User.follower.has(following_id=user_id)
            )
        )
    paginate_stmt = paginate(page=page, limit=limit, statement=stmt)
    result = await session.scalars(paginate_stmt)
    return result.unique().all()


async def get_subscribe_users_recipes(
        user_id: int,
        recipes_limit: int,
        session: 'AsyncSession'
        ) -> Sequence[Recipe]:
    stmt = (
        select(Recipe)
        .where(Recipe.author_id == user_id)
        .limit(recipes_limit)
    )
    result = await session.scalars(stmt)
    return result.unique().all()


async def get_subscribe_users_recipes_count(
        user_id: int,
        session: 'AsyncSession'
        ) -> int:
    stmt = select(func.count()).select_from(Recipe).where(
        Recipe.author_id == user_id
    )
    result = await session.scalar(stmt)
    return result


async def get_subscribed_users_count(
        user_id: int,
        session: 'AsyncSession'
        ) -> int:
    stmt = select(func.count()).select_from(Follow).where(
        Follow.following_id == user_id
    )
    result = await session.scalar(stmt)
    return result


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
        await session.execute(stmt)
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
