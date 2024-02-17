import csv
from typing import Self

from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert as upsert

from config import csv_data_root
from config.db import AsyncSession
from src.hasher import Hasher
from src.models.recipes import (Favorite, Follow, Ingredient, PurchaseCart,
                                Recipe, Tag)
from src.models.users import User

CSV_PATH_TAGS = csv_data_root + 'tags.csv'
CSV_PATH_INGREDIENTS = csv_data_root + 'ingredients.csv'
CSV_PATH_USERS = csv_data_root + 'users.csv'


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

    @action(
        name='import_users_data',
        label='Импорт тестовых пользователей',
        confirmation_message='Вы уверенны, что хотите импортировать?',
        add_in_detail=True,
        add_in_list=True,
    )
    async def import_users_data(self: Self, request: Request):
        session = AsyncSession()
        with open(CSV_PATH_USERS, newline='') as file:
            csv_reader = csv.reader(file)
            users_data = [
                {'email': row[0],
                 'first_name': row[1],
                 'last_name': row[2],
                 'username': row[3],
                 'hashed_password': Hasher.get_password_hash(row[4])}
                for row in csv_reader if row
                ]
            stmt = upsert(User).values(users_data).on_conflict_do_nothing()
            await session.execute(stmt)
            await session.commit()
        return RedirectResponse(
                str(request.base_url) + 'admin/user/list',
                status_code=302,
            )


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
    column_sortable_list = ['id', 'name']

    @action(
        name='import_tag_data',
        label='Импорт тегов',
        confirmation_message='Вы уверенны, что хотите импортировать?',
        add_in_detail=True,
        add_in_list=True,
    )
    async def import_tag_data(self: Self, request: Request):
        session = AsyncSession()
        with open(CSV_PATH_TAGS, newline='') as file:
            csv_reader = csv.reader(file)
            tags_data = [
                {'name': row[0],
                 'color': row[1],
                 'slug': row[2]}
                for row in csv_reader if row
                ]
            stmt = upsert(Tag).values(tags_data).on_conflict_do_nothing()
            await session.execute(stmt)
            await session.commit()
        return RedirectResponse(
                str(request.base_url) + 'admin/tag/list',
                status_code=302,
            )


class IngredientAdmin(
    ModelView,
    AdminPermissions,
    model=Ingredient
):
    name = 'Ингредиент'
    name_plural = 'Ингредиенты'
    column_list = ['id', 'name', 'measurement_unit']
    page_size = 50
    form_columns = [
        'name',
        'measurement_unit'
    ]
    column_sortable_list = ['id', 'name']

    @action(
        name='import_ingredient_data',
        label='Импорт ингредиентов',
        confirmation_message='Вы уверенны, что хотите импортировать?',
        add_in_detail=True,
        add_in_list=True
    )
    async def import_ingredient_data(self: Self, request: Request):
        session = AsyncSession()
        with open(CSV_PATH_INGREDIENTS, newline='') as file:
            csv_reader = csv.reader(file)
            ingredients_data = [
                {'name': row[0],
                 'measurement_unit': row[1]}
                for row in csv_reader if row
                ]
            stmt = (
                upsert(Ingredient)
                .values(ingredients_data)
                .on_conflict_do_nothing()
            )
            await session.execute(stmt)
            await session.commit()
        return RedirectResponse(
                str(request.base_url) + 'admin/ingredient/list',
                status_code=302,
            )

    @action(
        name='delete_all_ingredients',
        label='Удалить все ингредиенты',
        confirmation_message='Вы уверенны, что нужно удалить все ингредиенты?',
        add_in_detail=True,
        add_in_list=True
    )
    async def delete_all_ingredients(self: Self, request: Request):
        session = AsyncSession()
        stmt = delete(Ingredient)
        await session.execute(stmt)
        await session.commit()
        return RedirectResponse(
                str(request.base_url) + 'admin/ingredient/list',
                status_code=302,
            )


class FollowAdmin(
    ModelView,
    AdminPermissions,
    model=Follow
):
    name = 'Подписки'
    name_plural = 'Подписки'
    # column_list = [c.name for c in Follow.__table__.c]
    column_list = [Follow.id, Follow.follower_id, Follow.following_id]
    form_columns = [
        Follow.follower_id,
        Follow.following_id
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
