from fastapi import HTTPException, status
from src.schemas import users as users_schema
from src.models.users.models import User
from sqlalchemy import select
# from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.hasher import Hasher

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(
        session: 'AsyncSession',
        email: str
        ) -> User | None:
    """Получение пользователя из базы данных по email."""
    stmt = (
        select(User).where(User.email == email)
    )
    result = await session.scalars(stmt)
    return result.first()


# async def compare_incomming_token_with_db_token(
#         session: 'AsyncSession',
#         token: str,
#         email: str
# ) -> bool:
#     """Проверяет полученный из реквеста токен
#     с токеном сохраненным в базу данных."""
#     user = await get_user_by_email(session, email)
#     stmt = (
#         select(user).where(user.token == token)
#     )
#     result = await session.scalar(stmt)
#     return bool(result)


async def get_user(
        session: 'AsyncSession',
        user_id: int
        ) -> User | None:
    """Получить пользователя по id из базы данных."""
    stmt = (
        select(User).select_from(User).where(User.id == user_id))
    # ).options(
    #         joinedload(User.recipe).joinedload(User.following)
    #     )
    result = await session.scalars(stmt)
    return result.unique().first()


async def get_users(session: 'AsyncSession') -> Sequence[User]:
    """Получить список всех пользователей из базы данных."""
    stmt = select(User)
    result = await session.scalars(stmt)
    return result.unique().all()


async def create_user(
        session: 'AsyncSession',
        user_schema: users_schema.CreateUserSchema
        ) -> User:
    """Создать пользователя в базе данных."""
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
    """Изменить текущий пароль на новый в базе данных."""
    user = await get_user(session, user_id)
    if user is None:
        return None
    user.hashed_password = current_password
    await session.commit()
    return user


async def add_token_to_user_instance(
        session: 'AsyncSession',
        user: User,
        login_token: str
) -> bool:
    """Сохраняем текущий токен пользователю в базу данных."""
    user = await get_user(
        session=session,
        user_id=user.id,
    )
    if user is None:
        return False
    user.token = login_token
    user.is_authenticated = True
    await session.commit()
    return True


async def delete_token_from_user_instance(
        session: 'AsyncSession',
        user: User,
) -> bool:
    """Удаляем текущий токен пользователя из базы данных."""
    user = await get_user(session, user.id)
    if user is None:
        return False
    user.token = None
    user.is_authenticated = False
    await session.commit()
    return True
