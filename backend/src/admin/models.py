from fastapi import FastAPI
from sqladmin import Admin, ModelView
from backend.config.db import sync_engine
from backend.src.models.users.models import User
from backend.src.models.recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Follow,
    Favorite
)

app = FastAPI()
admin = Admin(app, sync_engine)


class UserAdmin(ModelView, model=User):
    column_list = ['__all__']


class RecipeAdmin(ModelView, model=Recipe):
    column_list = ['__all__']


class TagAdmin(ModelView, model=Tag):
    column_list = ['__all__']


class IngredientAdmin(ModelView, model=Ingredient):
    column_list = ['__all__']


class FollowAdmin(ModelView, model=Follow):
    column_list = ['__all__']


class FavoriteAdmin(ModelView, model=Favorite):
    column_list = ['__all__']


admin.add_view(UserAdmin)
admin.add_view(RecipeAdmin)
admin.add_view(TagAdmin)
admin.add_view(IngredientAdmin)
admin.add_view(FollowAdmin)
admin.add_view(FavoriteAdmin)
