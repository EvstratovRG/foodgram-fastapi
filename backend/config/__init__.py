import pathlib
from functools import lru_cache

from config.settings import SiteSettings, ApplicationSettings, DatabaseSettings

base_dir: str = pathlib.Path(__file__).parent.parent.as_posix()


@lru_cache
def get_app_config() -> ApplicationSettings:
    return ApplicationSettings()


@lru_cache
def get_site_config() -> SiteSettings:
    return SiteSettings()


@lru_cache
def get_db_config() -> DatabaseSettings:
    return DatabaseSettings()


app_config = get_app_config()
site_config = get_site_config()
db_config = get_db_config()

media_root: str = base_dir + app_config.media
