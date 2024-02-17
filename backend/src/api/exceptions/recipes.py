from fastapi import status
from fastapi.exceptions import HTTPException

RecipeNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Рецепт с таким id - не найден.'
)
ImageLoad = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Загрузка изображения пошла не по плану.'
)
ThroughEntity = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Ошибка при создании many-to-many.'
)
BadRequest = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='При загрузке рецептов произошла ошибка.'
)
IngredientNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Ингредиент с таким id - не найден.'
)
BadRequestUpdate = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='При попытке обновить рецепт произошла ошибка.'
)
