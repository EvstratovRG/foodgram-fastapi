from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_async_session
from src.api.constants.descriptions import carts as cart_descriptions
from src.api.constants.responses import carts as cart_responses
from src.api.constants.summaries import carts as cart_summaries
from src.api.endpoints.users import get_me
from src.api.exceptions import recipes as recipe_exceptions
from src.api.exceptions import users as user_exceptions
from src.models.users import User
from src.queries import carts as cart_queries
from src.schemas import recipes as recipe_schemas

router = APIRouter(prefix="/recipes", tags=["/recipes"])


@router.get(
    "/download_shopping_cart/",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    summary=cart_summaries.downloading_shopping_cart,
    responses=cart_responses.download_shopping_cart,
)
async def download_shopping_cart(
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    shopping_cart: list[str] = await cart_queries.shopping_cart(
        user_id=current_user.id,
        session=session
    )
    if shopping_cart is None:
        raise user_exceptions.UserNotFound
    filepath = "product_cart.txt"
    with open(filepath, "w") as cart:
        import re
        pattern = (r"[\(\)']")
        cart.write("Список продуктов\n\n")
        for elem in shopping_cart:
            elem = re.sub(
                pattern=pattern,
                repl="",
                string=str(elem)
            )
            cart.write(elem + '\n')
    return filepath


@router.post(
    "/{recipe_id}/shopping_cart/",
    status_code=status.HTTP_201_CREATED,
    response_model=recipe_schemas.PurchaseCart,
    summary=cart_summaries.adding_recipe_to_cart,
    responses=cart_responses.add_recipe_to_shopping_cart,
)
async def add_to_shopping_cart(
    recipe_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    recipe = await cart_queries.add_to_shopping_cart(
        current_user_id=current_user.id,
        recipe_id=recipe_id,
        session=session
    )
    if recipe is None:
        raise recipe_exceptions.RecipeNotFound
    return recipe


@router.delete(
    "/{recipe_id}/shopping_cart/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=cart_summaries.delete_recipe_from_the_cart,
    responses=cart_responses.delete_recipe_from_shopping_cart,
    response_description=cart_descriptions.delete_recipe_from_cart,
)
async def del_from_shopping_cart(
    recipe_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
):
    is_deleted = await cart_queries.del_from_shopping_cart(
        current_user_id=current_user.id,
        recipe_id=recipe_id,
        session=session
    )
    if not is_deleted:
        raise recipe_exceptions.RecipeNotFound
    return None
