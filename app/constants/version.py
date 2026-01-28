from os import name
from platform import platform, release, system
from sys import version
from typing import Final

# Current Python version.
PYTHON_VERSION: Final[str] = version

# Complete details about the operating system.
OPERATING_SYSTEM: Final[str] = platform()
OPERATING_SYSTEM_NAME: Final[str] = system()
OPERATING_SYSTEM_ALT: Final[str] = name
SYSTEM_VERSION: Final[str] = release()

WINDOWS: Final[str] = "nt"
MACOS: Final[str] = "posix"
