from fastapi import APIRouter, Depends, status
from typing import Any
from src.models.users.models import User
from src.queries import favorites as favorite_queries
from src.schemas import recipes as recipe_schemas
from src.schemas import base as base_schemas
from src.api.exceptions import recipes as recipe_exceptions
from src.api.endpoints.users import get_me
from config.db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/recipes", tags=["/recipes"])


@router.post(
    "/{recipe_id}/favorite/",
    status_code=status.HTTP_201_CREATED,
    response_model=(
        recipe_schemas.FavoriteRecipeSchema |
        base_schemas.ExceptionSchema
    )
)
async def favorite(
    recipe_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    favorite = await favorite_queries.favorite(
        current_user_id=current_user.id,
        recipe_id=recipe_id,
        session=session
    )
    if favorite is None:
        raise recipe_exceptions.RecipeNotFoundException
    return favorite


@router.delete(
    "/{recipe_id}/favorite/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unfavorite(
    recipe_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    unfavor = await favorite_queries.unfavorite(
        current_user_id=current_user.id,
        recipe_id=recipe_id,
        session=session
    )
    if not unfavor:
        raise recipe_exceptions.RecipeNotFoundException
    return None
