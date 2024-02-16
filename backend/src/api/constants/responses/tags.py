from src.api.constants.descriptions import tags as tag_descriptions
from src.api.constants.examples import tags as tag_examples
from src.schemas import recipes as recipe_schemas


get_tags_200 = {
    200: {
        "model": list[recipe_schemas.BaseTagSchema],
        "description": tag_descriptions.get_tags_200,
        "content": {
            "application/json": {
                "example": tag_examples.get_tags_200_example,
            }
        }
    }
}

get_tag_200 = {
    200: {
        "model": recipe_schemas.BaseTagSchema,
        "description": tag_descriptions.get_tag_200,
        "content": {
            "application/json": {
                "example": tag_examples.get_tag_200_example,
            }
        }
    }
}

get_tags = {
    **get_tags_200
}

get_tag = {
    **get_tag_200
}
