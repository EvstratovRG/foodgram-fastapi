from src.api.constants.descriptions import favorites as favorite_descriptions
from src.api.constants.examples import favorites as favorite_examples
from src.schemas import recipes as recipe_schemas

create_favorite_recipe_201 = {
    201: {
        "model": recipe_schemas.FavoriteRecipeSchema,
        "description": favorite_descriptions.favorite_recipe_201,
        "content": {
            "application/json": {
                "example": favorite_examples.favorite_recipe_example_201,
            }
        }
    }
}

delete_favorite_recipe_204 = {
    204: {"content": {"No content": {"example": ""}}}
}


create_favorite_recipe = {
    **create_favorite_recipe_201
}

delete_favorite_recipe = {
    **delete_favorite_recipe_204
}
