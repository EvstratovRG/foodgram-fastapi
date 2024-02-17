from src.api.constants.descriptions import \
    ingredients as ingredient_descriptions
from src.api.constants.examples import ingredients as ingredient_examples
from src.schemas import recipes as recipe_schemas

get_ingredients_200 = {
    200: {
        "model": list[recipe_schemas.BaseIngredientSchema],
        "description": ingredient_descriptions.get_ingredients_200,
        "content": {
            "application/json": {
                "example": ingredient_examples.get_ingredients_200_example,
            }
        }
    }
}

get_ingredient_200 = {
    200: {
        "model": recipe_schemas.BaseIngredientSchema,
        "description": ingredient_descriptions.get_ingredient_200,
        "content": {
            "application/json": {
                "example": ingredient_examples.get_ingredient_200_example,
            }
        }
    }
}

get_ingredients = {
    **get_ingredients_200
}

get_ingredient = {
    **get_ingredient_200
}
