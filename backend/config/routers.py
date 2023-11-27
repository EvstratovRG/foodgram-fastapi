from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    from backend.src.api.endpoints.users import router as users_router
    from backend.src.api.endpoints.tags import router as tags_touter
    from backend.src.api.endpoints.ingredients import router as ingredients_router
    from backend.src.api.endpoints.recipes import router as recipe_router

    routers: list[APIRouter] = list()

    routers.append(ingredients_router)
    routers.append(users_router)
    routers.append(tags_touter)
    routers.append(recipe_router)

    return routers
