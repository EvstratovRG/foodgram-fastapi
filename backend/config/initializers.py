from fastapi import FastAPI
from sqladmin import Admin


def init_app() -> FastAPI:
    from config import get_app_config

    app_config = get_app_config()

    app = FastAPI(**app_config.model_dump())
    return app


def init_routers(application: FastAPI) -> None:
    from config.routers import get_routers

    for router in get_routers():
        application.include_router(router, prefix='/api')


def init_admin(application: FastAPI) -> None:
    from config.db import sync_engine
    from src.admin.models import (
        UserAdmin,
        RecipeAdmin,
        TagAdmin,
        IngredientAdmin,
        FollowAdmin,
        FavoriteAdmin,
        PurchaseCartAdmin,
    )
    admin = Admin(application, sync_engine)
    admin.add_view(UserAdmin)
    admin.add_view(RecipeAdmin)
    admin.add_view(TagAdmin)
    admin.add_view(IngredientAdmin)
    admin.add_view(FollowAdmin)
    admin.add_view(FavoriteAdmin)
    admin.add_view(PurchaseCartAdmin)
