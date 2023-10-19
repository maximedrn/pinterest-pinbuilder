# -*- coding: utf-8 -*-
# app/constants/copyright.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from datetime import date
from typing import Final

from app.constants.colors import COLORAMA_YELLOW, COLORAMA_RESET
from app.constants.version import TOOL_VERSION


__current_year: int = date.today().year
COPYRIGHT: Final[str] = (
    f'{COLORAMA_YELLOW}Copyright © 2022-{__current_year} '
    'Pinterest Pinbuilder. All rights reserved. Any distribution, '
    'modification or commercial use is strictly prohibited.\n'
    f'Version {TOOL_VERSION}.{COLORAMA_RESET}'
)
