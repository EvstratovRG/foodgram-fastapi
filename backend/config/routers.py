from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    from src.api.endpoints.users import router as users_router
    from src.api.endpoints.tags import router as tags_touter
    from src.api.endpoints.ingredients import router as ingredients_router
    from src.api.endpoints.recipes import router as recipe_router
    from src.api.endpoints.follows import router as follow_router
    from src.api.endpoints.auth import router as auth_router
    from src.api.endpoints.favorites import router as favorite_router
    from src.api.endpoints.carts import router as cart_router

    routers: list[APIRouter] = list()

    routers.append(ingredients_router)
    routers.append(follow_router)
    routers.append(users_router)
    routers.append(tags_touter)
    routers.append(recipe_router)
    routers.append(auth_router)
    routers.append(favorite_router)
    routers.append(cart_router)
    return routers
