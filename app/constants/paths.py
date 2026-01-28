from os.path import join
from typing import Final

from app.constants.version import OPERATING_SYSTEM_ALT, WINDOWS

# Local front-end server address.
FRONTEND_HOST: Final[str] = "localhost"
FRONTEND_PORT: Final[int] = 8000
FRONTEND_FOLDER: Final[str] = "public"
FRONTEND_FILE: Final[str] = "index.html"
FRONTEND_BROWSER: Final[str] = "chrome"
BROWSER_ARGUMENTS: Final[list[str]] = ["--disable-gpu", "--disable-http-cache"]
ALLOWED_EXTENSIONS: Final[list[str]] = [".html", ".css", ".js"]

# Location of the tool's main directories and files.
ASSETS_FOLDER: Final[str] = "assets"
DATA_FOLDER: Final[str] = "data"
TEMP_FOLDER: Final[str] = "temp"
UPLOAD_FOLDER: Final[str] = join(DATA_FOLDER, "upload")
LOG_FOLDER: Final[str] = join(FRONTEND_FOLDER, "logs")
COOKIES_FILE: Final[str] = join(ASSETS_FOLDER, "cookies.json")
__extension: str = ".exe" if OPERATING_SYSTEM_ALT == WINDOWS else ""
WEBDRIVER_FILE: Final[str] = join(ASSETS_FOLDER, "chromedriver") + __extension
