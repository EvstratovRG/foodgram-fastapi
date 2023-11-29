from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hasher:
    """Класс с методами хеширования и дехеширования паролей."""
    @staticmethod
    def verify_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Метод хеширования пароля."""
        return pwd_context.hash(password)
