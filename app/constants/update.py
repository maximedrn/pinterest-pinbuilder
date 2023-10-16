# -*- coding: utf-8 -*-
# app/constants/update.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import List

from app.constants.paths import FRONTEND_FOLDER, LOG_FOLDER


# Various directories and files to be deleted before updating the tool.
PATHS_TO_REMOVE: List[str] = [
    '__pycache__',
    'app',
    FRONTEND_FOLDER,
    LOG_FOLDER,
    'main.py',
    'run.bat',
    'run.sh',
    'requirements.txt'
]


# Various backend URLs to update the tool, retrieve 
# the latest version and changelog.
__gitfront_url: str = 'https://gitfront.io/r/{}/{}/{}/raw/'
__gitfront_account_name: str = 'Maksyme'
__repository_id: str = 'zEqkryPh3ET9'
__repository_name: str = 'pinterest-pinbuilder-backend'
__backend_url: str = __gitfront_url.format(
    __gitfront_account_name, __repository_id, __repository_name)

VERSION_URL: str = __backend_url + 'version.txt'
CHANGELOG_URL: str = __backend_url + 'changelog.txt'
UPDATE_URL: str = __backend_url + 'pinterest-pinbuilder.zip'
