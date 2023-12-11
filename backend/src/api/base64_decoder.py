import base64
from config import media_root
from src.api.exceptions.recipes import ImageLoadException
from datetime import datetime


def base64_decoder(data: str) -> str | None:
    if data.startswith('data:image'):
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            image_binary: bytes = base64.b64decode(imgstr)
            filename = f"{datetime.now()}.{ext}"
            file_path = media_root + filename
            with open(file_path, "wb") as file:
                file.write(image_binary)
            return filename
        except BaseException as exc:
            raise ImageLoadException(exc)
    return None
