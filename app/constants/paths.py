# -*- coding: utf-8 -*-
# app/constants/paths.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from os import name
from os.path import join
from typing import Final, List


# Local front-end server address.
FRONTEND_HOST: Final[str] = 'localhost'
FRONTEND_PORT: Final[int] = 8000
FRONTEND_FOLDER: Final[str] = 'public'
FRONTEND_FILE: Final[str] = 'index.html'
FRONTEND_BROWSER: Final[str] = 'chrome'
BROWSER_ARGUMENTS: Final[List[str]] = [
    '--disable-gpu',
    '--disable-http-cache'
]
ALLOWED_EXTENSIONS: Final[List[str]] = [
    '.html',
    '.css',
    '.js'
]

# Location of the tool's main directories and files.
ASSETS_FOLDER: Final[str] = 'assets'
DATA_FOLDER: Final[str] = 'data'
TEMP_FOLDER: Final[str] = 'temp'
UPLOAD_FOLDER: Final[str] = join(DATA_FOLDER, 'upload')
LOG_FOLDER: Final[str] = join(FRONTEND_FOLDER, 'logs')
LICENSE_KEY_FILE: Final[str] = join(ASSETS_FOLDER, 'license_key.json')
COOKIES_FILE: Final[str] = join(ASSETS_FOLDER, 'cookies.json')
__extension: str = '.exe' if name == 'nt' else ''
WEBDRIVER_FILE: Final[str] = join(ASSETS_FOLDER, 'chromedriver') + __extension
