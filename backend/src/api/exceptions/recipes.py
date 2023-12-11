from fastapi.exceptions import HTTPException
from fastapi import status


RecipeNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Рецепт с таким id - не найден.'
)


ImageLoadException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Загрузка изображения пошла не по плану.'
)

ThroughEntityException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Ошибка при создании many-to-many.'
)
