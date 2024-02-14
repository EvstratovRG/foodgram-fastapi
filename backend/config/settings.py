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
    token_expire: int
    algorithm: str
    media: str
    data: str


class DatabaseSettings(BaseSettings):

    # model_config = SettingsConfigDict(
    #     env_file=APP_PATH / 'dotenv' / '.env',
    # )
    model_config = SettingsConfigDict(
        env_file=APP_PATH / 'dotenv' / '.env-local',
    )

    postgres_host: str
    postgres_user: str
    postgres_port: int
    postgres_db: str
    postgres_password: str
    allowed_hosts: str

    @property
    def database_url_asyncpg(self):
        return (f'postgresql+asyncpg://'
                f'{self.postgres_user}:'
                f'{self.postgres_password}@'
                f'{self.postgres_host}:'
                f'{self.postgres_port}/'
                f'{self.postgres_db}')

    @property
    def database_url_psycopg(self):
        return (f'postgresql+psycopg2://'
                f'{self.postgres_user}:'
                f'{self.postgres_password}@'
                f'{self.postgres_host}:'
                f'{self.postgres_port}/'
                f'{self.postgres_db}')
