from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    # from src.api.recipes.recipes import router as recipes_router
    from src.api.users.users import router as users_router

    routers: list[APIRouter] = list()

    # добавляем сюда роутеры
    # routers.append(recipes_router)
    routers.append(users_router)

    return routers
