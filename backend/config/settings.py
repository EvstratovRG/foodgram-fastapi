import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_PATH = pathlib.Path(__file__).parent.parent.parent


class SiteSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=APP_PATH / 'dotenv' / '.env-site',
    )

    host: str
    port: int
    log_level: str
    reload: bool


class ApplicationSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=APP_PATH / 'dotenv' / '.env-app',
    )

    title: str
    description: str
    debug: bool
    version: str
    secret: str


class DatabaseSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=APP_PATH / 'dotenv' / '.env',
    )

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    @property
    def database_url_asyncpg(self):
        return (f'postgresql+asyncpg://'
                f'{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/'
                f'{self.POSTGRES_DB}')

    @property
    def database_url_psycopg(self):
        return (f'postgresql+psycopg2://'
                f'{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/'
                f'{self.POSTGRES_DB}')
