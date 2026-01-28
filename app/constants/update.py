from typing import Final

from app.constants.paths import FRONTEND_FOLDER, LOG_FOLDER

# Various directories and files to be deleted before updating the tool.
PATHS_TO_REMOVE: Final[list[str]] = [
    "__pycache__",
    "app",
    FRONTEND_FOLDER,
    LOG_FOLDER,
    "main.py",
    "run.bat",
    "run.sh",
    "requirements.txt",
]
