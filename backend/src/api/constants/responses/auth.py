from src.schemas import base as base_schemas
from src.api.constants.descriptions import auth as auth_descriptions
from src.api.constants.examples import auth as auth_examples


post_token_201 = {
    201: {
        "model": base_schemas.Token,
        "description": auth_descriptions.post_token_201,
        "content": {
            "application/json": {
                "example": auth_examples.post_token_201_example,
            }
        }
    }
}

delete_token_204 = {
    204: {"content": {"No content": {"example": ""}}}
}

post_token = {
    **post_token_201
}

delete_token = {
    **delete_token_204
}
