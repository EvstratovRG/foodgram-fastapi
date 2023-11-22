from fastapi import APIRouter


def get_routers() -> list[APIRouter]:
    from src.api.recipes import recipes_router
    from src.api.users import users_router

    routers: list[APIRouter] = list()

    # добавляем сюда роутеры
    routers.append(recipes_router)
    routers.append(users_router)

    return routers
