from fastapi import APIRouter, Depends, status, Request
from typing import Any
from src.models.users import User
from src.queries import favorites as favorite_queries
from src.schemas import recipes as recipe_schemas
from src.api.exceptions import recipes as recipe_exceptions
from src.api.endpoints.users import get_me
from config.db import get_async_session
from src.api.constants.summaries import favorites as favorite_summaries

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/recipes", tags=["/recipes"])


@router.post(
    "/{recipe_id}/favorite/",
    status_code=status.HTTP_201_CREATED,
    summary=favorite_summaries.adding_recipe_to_favorites
)
async def favorite(
    request: Request,
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
    r_schema = recipe_schemas.RecipeBaseSchema.model_validate(favorite)
    r_schema.image_convert(request)
    return recipe_schemas.FavoriteRecipeSchema(
        id=r_schema.id,
        name=r_schema.name,
        image=r_schema.image,
        cooking_time=r_schema.cooking_time
    )


@router.delete(
    "/{recipe_id}/favorite/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=favorite_summaries.delete_recipe_from_favorites
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
