from fastapi.exceptions import HTTPException
from fastapi import status


UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Пользователь с таким id - не найден.'
)
AlreadyExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Пользователь с такими данными уже существует.'
)
SomethingGoesWrong = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Чётапошлонетак'
)
WrongСredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не верные имейл или пароль'
)
WrongPassword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Не верно введен пароль'
)
BadSubscribe = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Нельзя подписаться на самого себя!'
)
