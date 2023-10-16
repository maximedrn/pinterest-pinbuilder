# -*- coding: utf-8 -*-
# app/constants/version.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from platform import platform, release, system
from sys import version


# Latest version of the tool.
TOOL_VERSION: str = '1.1.0'

# Current Python version.
PYTHON_VERSION: str = version

# Complete details about the operating system.
OPERATING_SYSTEM: str = platform()
OPERATING_SYSTEM_NAME: str = system()
SYSTEM_VERSION: str = release()
