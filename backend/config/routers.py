from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    from src.api.endpoints.users import router as users_router
    from src.api.endpoints.tags import router as tags_touter
    from src.api.endpoints.ingredients import router as ingredients_router
    from src.api.endpoints.recipes import router as recipe_router

    routers: list[APIRouter] = list()

    routers.append(ingredients_router)
    routers.append(users_router)
    routers.append(tags_touter)
    routers.append(recipe_router)

    return routers
