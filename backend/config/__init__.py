import pathlib
from typing import Any

from backend.config.settings import SiteSettings, ApplicationSettings, DatabaseSettings

base_dir: str = pathlib.Path(__file__).parent.parent.as_posix()


app_config: dict[str, Any] = ApplicationSettings().model_dump()
site_config: dict[str, Any] = SiteSettings().model_dump()
db_config: dict[str, Any] = DatabaseSettings()
