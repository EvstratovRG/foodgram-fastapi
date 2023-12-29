from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from typing import Any
from src.models.users.models import User
from src.queries import carts as cart_queries
from src.schemas import recipes as recipe_schemas
from src.api.exceptions import users as user_exceptions
from src.api.exceptions import recipes as recipe_exceptions
from src.api.endpoints.users import get_me
from config.db import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/recipes", tags=["/recipes"])


@router.get(
    "/download_shopping_cart/",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse
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
        raise user_exceptions.SomethingGoesWrong
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
    response_model=recipe_schemas.PurchaseCart
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
        raise user_exceptions.SomethingGoesWrong
    return recipe


@router.delete(
    "/{recipe_id}/shopping_cart/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def del_from_shopping_cart(
    recipe_id: int,
    current_user: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    is_deleted = await cart_queries.del_from_shopping_cart(
        current_user_id=current_user.id,
        recipe_id=recipe_id,
        session=session
    )
    if not is_deleted:
        raise recipe_exceptions.RecipeNotFoundException
    return None
