from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
