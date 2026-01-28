from __future__ import annotations

from screeninfo import Monitor, get_monitors

from app.constants.screen import (
    HEIGHT_MULTIPLICATOR,
    MAX_HEIGHT,
    MAX_WIDTH,
    WIDTH_MULTIPLICATOR,
)


def get_interface_size() -> tuple[tuple[float, float], tuple[float, float]]:
    """Set the size of the interface and center it on the screen.

    Returns:
    --------
        tuple[tuple[float, float], tuple[float, float]]: A tuple containing
            two tuples - the first tuple represents the width and height of
            the interface, and the second tuple represents the position
            (x, y) to center the interface on the screen.
    """
    # Get the user's screen width and height.
    monitor: Monitor = get_monitors()[0]
    __user_screen_width: int = monitor.width
    __user_screen_height: int = monitor.height
    # Initialize the width and height based on maximum values and multipliers.
    width: float = MAX_WIDTH * WIDTH_MULTIPLICATOR  # Default.
    height: float = MAX_HEIGHT * HEIGHT_MULTIPLICATOR  # Default.
    width: float = min(width, __user_screen_width)
    height: float = min(height, __user_screen_height)
    # Calculate the position to center the interface on the screen.
    position: tuple[float, float] = (
        (__user_screen_width - width) / 2,
        (__user_screen_height - height) / 2,
    )
    return (width, height), position
