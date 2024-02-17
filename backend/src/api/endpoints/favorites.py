from typing import Any

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_async_session
from src.api.constants.responses import favorites as favorite_responses
from src.api.constants.summaries import favorites as favorite_summaries
from src.api.endpoints.users import get_me
from src.api.exceptions import recipes as recipe_exceptions
from src.models.users import User
from src.queries import favorites as favorite_queries
from src.schemas import recipes as recipe_schemas

router = APIRouter(prefix="/recipes", tags=["/recipes"])


@router.post(
    "/{recipe_id}/favorite/",
    status_code=status.HTTP_201_CREATED,
    responses=favorite_responses.create_favorite_recipe,
    summary=favorite_summaries.adding_recipe_to_favorites,
    response_model=recipe_schemas.FavoriteRecipeSchema
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
        raise recipe_exceptions.RecipeNotFound
    r_schema = recipe_schemas.RecipeBaseSchema.model_validate(favorite)
    r_schema.image_convert(request)
    return r_schema


@router.delete(
    "/{recipe_id}/favorite/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=favorite_responses.delete_favorite_recipe,
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
        raise recipe_exceptions.RecipeNotFound
    return None
