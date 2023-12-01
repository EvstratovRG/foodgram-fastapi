from fastapi import HTTPException, status
from src.schemas import users as users_schema
from src.models.users.models import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.hasher import Hasher

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(
        session: 'AsyncSession',
        email: str
        ) -> User | None:
    """Получение пользователя из бд по email."""
    stmt = (
        select(User).where(User.email == email)
    )
    result = await session.scalars(stmt)
    return result.first()


async def get_user(
        session: 'AsyncSession',
        user_id: int
        ) -> User | None:
    stmt = (
        select(User).select_from(User).where(User.id == user_id))
    # ).options(
    #         joinedload(User.recipe).joinedload(User.following)
    #     )
    result = await session.scalars(stmt)
    return result.unique().first()


async def get_users(session: 'AsyncSession') -> Sequence[User]:
    stmt = select(User)
    result = await session.scalars(stmt)
    return result.unique().all()


async def create_user(
        session: 'AsyncSession',
        user_schema: users_schema.CreateUserSchema
        ) -> User:
    user = User(
        username=user_schema.username,
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        email=user_schema.email,
        hashed_password=Hasher.get_password_hash(user_schema.password)
    )
    try:
        session.add(user)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    return user


async def update_password(
        session: 'AsyncSession',
        user_id: int,
        current_password: str
        ) -> User | None:
    user = await get_user(session, user_id)
    if user is None:
        return None
    user.hashed_password = current_password
    await session.commit()
    return user


# async def delete_user(
#         session: 'AsyncSession',
#         user_id: int
#         ) -> bool | None:
#     user = await get_user(session, user_id)
#     if user is None:
#         return None
#     try:
#         await session.delete(user)
#         await session.commit()
#     except IntegrityError:
#         return False
#     return True


# async def delete_all_users(
#         session: 'AsyncSession',
#         ) -> bool | None:
#     users = select(User)
#     try:
#         session.delete(users)
#     except IntegrityError:
#         return False
#     return True
