# -*- coding: utf-8 -*-
# app/common/screen_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from tkinter import Tk
from typing import Tuple

from app.constants.screen import (
    HEIGHT_MULTIPLICATOR, MAX_HEIGHT, MAX_WIDTH, WIDTH_MULTIPLICATOR)


def get_interface_size() -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Set the size of the interface and center it on the screen.

    Returns:
    --------
        Tuple[Tuple[float, float], Tuple[float, float]]: A tuple containing
            two tuples - the first tuple represents the width and height of
            the interface, and the second tuple represents the position
            (x, y) to center the interface on the screen.
    """
    # Get the user's screen width and height.
    __user_screen_width: int = Tk().winfo_screenwidth()
    __user_screen_height: int = Tk().winfo_screenheight()
    # Initialize the width and height based on maximum values and multipliers.
    width: float = MAX_WIDTH * WIDTH_MULTIPLICATOR  # Default.
    height: float = MAX_HEIGHT * HEIGHT_MULTIPLICATOR  # Default.
    width: float = min(width, __user_screen_width)
    height: float = min(height, __user_screen_height)
    # Calculate the position to center the interface on the screen.
    position: Tuple[float, float] = (
        (__user_screen_width - width) / 4,
        ( __user_screen_height - height) / 4)
    return (width, height), position
