from sqlalchemy import select, insert
from typing import TYPE_CHECKING
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status
from src.queries import recipes as recipe_queries
from src.models.recipes import Recipe, Favorite
from sqlalchemy.exc import SQLAlchemyError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def favorite(
    recipe_id: int,
    current_user_id: int,
    session: 'AsyncSession'
) -> Recipe | None:
    stmt = insert(Favorite).values(
        user_id=current_user_id,
        recipe_id=recipe_id
    )
    try:
        favor = await session.scalars(stmt)
        if not favor:
            raise IntegrityError('Не удалось сделать рецепт избранным')
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    await session.commit()
    recipe = await recipe_queries.get_recipe(session, recipe_id)
    return recipe


async def unfavorite(
    recipe_id: int,
    current_user_id: int,
    session: 'AsyncSession'
) -> bool:
    favor = select(Favorite).where(
        Favorite.recipe_id == recipe_id,
        Favorite.user_id == current_user_id
    )
    result = await session.scalars(favor)
    if favor is None:
        return False
    try:
        await session.delete(result.first())
        await session.commit()
    except SQLAlchemyError:
        return False
    return True
