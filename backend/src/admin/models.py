from sqladmin import ModelView, action
from src.models.users.models import User
from src.models.recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Follow,
    Favorite,
    PurchaseCart
)


class AdminPermissions:
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class UserAdmin(
    ModelView,
    AdminPermissions,
    model=User
):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_list = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    form_columns = [
        'username',
        'first_name',
        'last_name',
        'email',
        'hashed_password',
        'is_superuser',
        'is_active',
        'is_staff'
    ]


class RecipeAdmin(
    ModelView,
    AdminPermissions,
    model=Recipe
):
    name = 'Рецепт'
    name_plural = 'Рецепты'
    column_list = ['id', 'name', 'ingredients', 'tags', 'author']
    column_formatters = {Recipe.author: lambda m, a: m.author.username}
    column_sortable_list = [Recipe.name, Recipe.author, Recipe.id]
    icon = "image"
    form_columns = [
        'author',
        'tags',
        'ingredients',
        'name',
        'text',
        'cooking_time',
        'image'
    ]


class TagAdmin(
    ModelView,
    AdminPermissions,
    model=Tag
):
    name = 'Тег'
    name_plural = 'Теги'
    column_list = ['id', 'name', 'color']
    form_columns = [
        'name',
        'color',
        'slug'
    ]
    # @action(
    #     name='import_tag_data',
    #     label='Импорт тегов'
    #     confirmation_message='Вы уверенны, что хотите импортировать?',
    #     add_in_detail=True,
    #     add_in_list=True
    # )
    # async def import_tag_data(self, request):


class IngredientAdmin(
    ModelView,
    AdminPermissions,
    model=Ingredient
):
    name = 'Ингредиент'
    name_plural = 'Ингредиенты'
    column_list = ['id, name, measurement_unit']
    form_columns = [
        'name',
        'measurement_unit'
    ]


class FollowAdmin(
    ModelView,
    AdminPermissions,
    model=Follow
):
    name = 'Подписки'
    name_plural = 'Подписки'
    # column_list = [c.name for c in Follow.__table__.c]
    column_list = ['__all__']
    form_columns = [
        'follower_id',
        'following_id'
    ]


class FavoriteAdmin(
    ModelView,
    AdminPermissions,
    model=Favorite
):
    name = 'Избранный рецепт'
    name_plural = 'Избранные рецепты'
    # column_list = [c.name for c in Favorite.__table__.c]
    column_list = ['__all__']
    form_columns = [
        'user_id',
        'recipe_id'
    ]


class PurchaseCartAdmin(
    ModelView,
    AdminPermissions,
    model=PurchaseCart
):
    name = 'Корзина'
    name_plural = 'Корзины'
    # colomn_list = [c.name for c in PurchaseCart.__table__.c]
    column_list = ['__all__']
    form_columns = [
        'user_id',
        'recipe_id'
    ]
