# -*- coding: utf-8 -*-
# app/constants/colors.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from importlib.abc import Loader
from pkgutil import find_loader


COLORAMA_RED = COLORAMA_YELLOW = COLORAMA_RESET = ''

__colorama: Loader | None = find_loader('colorama')
if __colorama:
    from colorama import init, Fore, Style


    # Create the instance of the Colorama module.
    # Conversion and autoreset are activated.
    init(convert=True, autoreset=True)

    # Set text color to red in the command prompt.
    COLORAMA_RED: str = Fore.RED
    # Set text color to red in the command prompt.
    COLORAMA_YELLOW: str = Fore.YELLOW
    # Reset any color attribute in command prompt.
    COLORAMA_RESET: str = Style.RESET_ALL    


# Hexadecimal colors for HTML/CSS.
GREEN: str = '#00a500'
RED: str = '#a50000'
YELLOW: str = '#deaa00'
