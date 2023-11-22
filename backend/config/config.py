from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib

APP_PATH = pathlib.Path(__file__).parent.parent


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=APP_PATH / '.env')

    DB_HOST: str
    DB_USER: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str

    @property
    def database_url_asyncpg(self):
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:'
                f'{self.DB_PASS}@'
                f'{self.DB_HOST}:'
                f'{self.DB_PORT}/'
                f'{self.DB_NAME}')

    @property
    def database_url_psycopg(self):
        return (f'postgresql+psycopg://'
                f'{self.DB_USER}:'
                f'{self.DB_PASS}@'
                f'{self.DB_HOST}:'
                f'{self.DB_PORT}/'
                f'{self.DB_NAME}')


settings = Settings()
