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
from typing import List


# Local front-end server address.
FRONTEND_HOST: str = 'localhost'
FRONTEND_PORT: int = 8000
FRONTEND_FOLDER: str = 'public'
FRONTEND_FILE: str = 'index.html'
FRONTEND_BROWSER: str = 'chrome'
BROWSER_ARGUMENTS: List[str] = [
    '--disable-gpu',
    '--disable-http-cache'
]
ALLOWED_EXTENSIONS: List[str] = [
    '.html',
    '.css',
    '.js'
]

# Location of the tool's main directories and files.
ASSETS_FOLDER: str = 'assets'
DATA_FOLDER: str = 'data'
TEMP_FOLDER: str = 'temp'
UPLOAD_FOLDER: str = join(DATA_FOLDER, 'upload')
LOG_FOLDER: str = join(FRONTEND_FOLDER, 'logs')
LICENSE_KEY_FILE: str = join(ASSETS_FOLDER, 'license_key.json')
COOKIES_FILE: str = join(ASSETS_FOLDER, 'cookies.json')
WEBDRIVER_FILE: str = join(ASSETS_FOLDER, 'chromedriver') \
    + '.exe' if name == 'nt' else ''
