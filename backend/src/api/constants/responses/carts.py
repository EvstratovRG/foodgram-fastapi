from src.api.constants.descriptions import carts as cart_descriptions
from src.api.constants.examples import carts as cart_examples
from src.schemas import recipes as recipe_schemas

add_recipe_to_shopping_cart_201 = {
    201: {
        "model": recipe_schemas.FavoriteRecipeSchema,
        "description": cart_descriptions.add_recipe_to_shopping_cart_201,
        "content": {
            "application/json": {
                "example": cart_examples.add_recipe_to_shopping_cart_example,
            }
        }
    }
}

delete_recipe_from_shopping_cart_204 = {
    204: {"content": {"No content": {"example": ""}}}
}

download_shopping_cart_200 = {
    200: {"content": {"product_cart.txt": {"example": ""}},
          "description": "Выгрузка списка ингредиентов из "
                         "добавленных в карзину рецептов."}
}

add_recipe_to_shopping_cart = {
    **add_recipe_to_shopping_cart_201
}

delete_recipe_from_shopping_cart = {
    **delete_recipe_from_shopping_cart_204
}

download_shopping_cart = {
    **download_shopping_cart_200
}
