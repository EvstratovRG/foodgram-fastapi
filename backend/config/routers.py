from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    # from src.api.recipes.recipes import router as recipes_router
    from src.api.endpoints.users import router as users_router
    from src.api.endpoints.tags import router as tags_touter

    routers: list[APIRouter] = list()

    # добавляем сюда роутеры
    # routers.append(recipes_router)
    routers.append(users_router)
    routers.append(tags_touter)

    return routers
