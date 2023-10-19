# -*- coding: utf-8 -*-
# app/constants/processes.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import Any, Dict, Final, List


# Names of the different processes stored in the manager.
# __html: str = '.html'
__json: str = '.json'
__login: str = 'login'
__upload: str = 'upload'
__create: str = 'create'

LOGIN_PROCESS: Final[str] = __login + __json
UPLOAD_PROCESS: Final[str] = __upload + __json
CREATE_PROCESS: Final[str] = __create + __json

PROCESSES: Final[List[str]] = [
    LOGIN_PROCESS,
    UPLOAD_PROCESS,
    CREATE_PROCESS
]

# Keys of the `manager` global dictionary.
MANAGER_PROCESSES: Final[str] = 'pid'
MANAGER_LICENSE_KEY: Final[str] = 'license_key'

MANAGER_DEFAULT_STATE: Final[Dict[str, Any]] = {
    MANAGER_LICENSE_KEY: '',
    MANAGER_PROCESSES: [],
    UPLOAD_PROCESS: False,
}