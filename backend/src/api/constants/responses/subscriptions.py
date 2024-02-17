from src.api.constants.descriptions import \
    subscriptions as subscription_descriptions
from src.api.constants.examples import subscriptions as subscription_examples
from src.pagination import schemas as pagination_schemas
from src.schemas import users as user_schemas

get_subscriptions_200 = {
    200: {
        "model": pagination_schemas.SubscibePagination,
        "description": subscription_descriptions.get_subscriptions_200,
        "content": {
            "application/json": {
                "example": subscription_examples.get_subscriptions_200_example,
            }
        }
    }
}

create_subscribe_201 = {
    201: {
        "model": user_schemas.GetSubscriptions,
        "description": subscription_descriptions.post_subscribe_201,
        "content": {
            "application/json": {
                "example": subscription_examples.subscribe_user_201_example,
            }
        }
    }
}

delete_subscribe_204 = {
    204: {"content": {"No content": {"example": ""}}}
}

get_subscriptions = {
    **get_subscriptions_200
}

create_subscribe = {
    **create_subscribe_201
}

delete_subscribe = {
    **delete_subscribe_204
}
