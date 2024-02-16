from src.api.constants.descriptions import recipes as recipe_descriptions
from src.api.constants.examples import recipes as recipe_examples
from src.pagination import schemas as pagination_schemas
from src.schemas import recipes as recipe_schemas


get_recipes_200 = {
    200: {
        "model": pagination_schemas.RecipePagination,
        "description": recipe_descriptions.get_recipes_200,
        "content": {
            "application/json": {
                "example": recipe_examples.get_recipes_200_example,
            }
        }
    }
}

get_recipe_200 = {
    200: {
        "model": recipe_schemas.RecipeBaseSchema,
        "description": recipe_descriptions.get_recipe_200,
        "content": {
            "application/json": {
                "example": recipe_examples.get_recipe_by_id_200_example,
            }
        }
    }
}

update_recipe_200 = {
    200: {
        "model": recipe_schemas.RecipeBaseSchema,
        "description": recipe_descriptions.patch_recipe_200,
        "content": {
            "application/json": {
                "example": recipe_examples.patch_recipe_by_id_200_example,
            }
        }
    }
}

create_recipe_201 = {
    201: {
        "model": recipe_schemas.RecipeBaseSchema,
        "description": recipe_descriptions.post_recipe_201,
        "content": {
            "application/json": {
                "example": recipe_examples.post_recipe_201_example,
            }
        }
    }
}

delete_recipe_204 = {
    204: {"content": {"No content": {"example": ""}}}
}

get_recipes = {
    **get_recipes_200
}

get_recipe = {
    **get_recipe_200
}

update_recipe = {
    **update_recipe_200
}

create_recipe = {
    **create_recipe_201
}

delete_recipe = {
    **delete_recipe_204
}
