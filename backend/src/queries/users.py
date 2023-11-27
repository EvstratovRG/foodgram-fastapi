from src.schemas import users as users_schema
from src.models.users.models import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from config.db import AsyncSession


async def get_user(
        session: 'AsyncSession',
        user_id: int
        ) -> User | None:
    stmt = (
        select(User).select_from(User).where(User.id == user_id).options(
            joinedload(User.recipes, User.following)
        ),
    )
    # is_subscribed = 
    result = await session.scalars(stmt)
    return result.first()


async def get_users(session: 'AsyncSession') -> Sequence[User]:
    stmt = select(User)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
        session: 'AsyncSession',
        user_schema: users_schema.CreateUserSchema
        ) -> User:
    user = User(
        username=user_schema.username,
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        email=user_schema.email,
    )
    session.add(user)
    await session.commit()
    return user


async def update_user(
        session: 'AsyncSession',
        user_id: int,
        user_schema: users_schema.UpdateUserSchema
        ) -> User | None:
    user = await get_user(session, user_id)
    if user is None:
        return None
    user.username = user_schema.username
    user.first_name = user_schema.first_name
    user.last_name = user_schema.last_name
    user.email = user_schema.email
    await user.commit()
    return user


async def delete_user(
        session: 'AsyncSession',
        user_id: int
        ) -> bool | None:
    user = await get_user(session, user_id)
    if user is None:
        return None
    try:
        await session.delete(user)
        await session.commit()
    except SQLAlchemyError:
        return False
    return True
