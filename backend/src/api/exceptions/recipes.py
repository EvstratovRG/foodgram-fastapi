from fastapi.exceptions import HTTPException
from fastapi import status


RecipeNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Рецепт с таким id - не найден.'
)
