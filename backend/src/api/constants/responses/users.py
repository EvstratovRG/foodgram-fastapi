from src.api.constants.descriptions import users as user_descriptions
from src.api.constants.examples import users as user_examples
from src.pagination import schemas as pagination_schemas
from src.schemas import users as user_schemas

get_users_200 = {
    200: {
        "model": pagination_schemas.UserPagination,
        "description": user_descriptions.get_users_200,
        "content": {
            "application/json": {
                "example": user_examples.get_users_200_example,
            }
        }
    }
}

get_user_200 = {
    200: {
        "model": user_schemas.UserBaseSchema,
        "description": user_descriptions.get_user_by_id_200,
        "content": {
            "application/json": {
                "example": user_examples.get_user_by_id_200_example,
            }
        }
    }
}

get_me_200 = {
    200: {
        "model": user_schemas.UserBaseSchema,
        "description": user_descriptions.get_me_200,
        "content": {
            "application/json": {
                "example": user_examples.get_me_200_example,
            }
        }
    }
}

create_user_201 = {
    201: {
        "model": user_schemas.UserBaseSchema,
        "description": user_descriptions.post_user_201,
        "content": {
            "application/json": {
                "example": user_examples.post_user_201_example,
            }
        }
    }
}

set_password_204 = {
    204: {"content": {"No content": {"example": ""}}}
}

get_users = {
    **get_users_200
}

get_user = {
    **get_user_200
}

get_me = {
    **get_me_200
}

create_user = {
    **create_user_201
}

set_password = {
    **set_password_204
}
