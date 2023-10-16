# -*- coding: utf-8 -*-
# app/utils/func.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from os import system, name
from sys import exit as sys_exit, version_info

from app.constants.colors import COLORAMA_RED, COLORAMA_RESET
from app.constants.messages import PYTHON_VERSION_ERROR
from app.constants.version import (
    TOOL_VERSION, PYTHON_VERSION, OPERATING_SYSTEM)


def cls() -> None:
    """Clear console from the command line.

    It uses the default system function:
        - "cls" if system is Windows.
        - "clear" is system is Linux or MacOS.
    """
    # Type the specific command using the system function.
    # "cls" if operating system is Windows, else "clear".
    system('cls' if name == 'nt' else 'clear')


def exit(message: str = '') -> None:
    """Exit and stop the process.

    Call the the exit method from the `sys` module.
    Change the text color to red before displaying
    the message at the end of the process.
    
    Parameters:
    -----------
        message (str, optional): The message to display before
            stopping the program. Defaults to ''.
    """
    sys_exit(COLORAMA_RED + message + COLORAMA_RESET)
    
    
def check_python_version() -> None:
    """Check if the current Python.
    
    Python version must be 3.8 or higher. If not, exit the program
    with an error message.

    Raises:
    -------
        SystemExit: If the Python version is not 3.8 or higher,
            the program exits with an error message.
    """
    if not version_info >= (3, 8):
        exit(PYTHON_VERSION_ERROR.format(PYTHON_VERSION))


def display_configuration() -> None:
    """Display the configuration information of the tool.

    This function prints the following information:
        - Version of the tool (`TOOL_VERSION`).
        - Version of Python (`PYTHON_VERSION`).
        - Operating system (`OPERATING_SYSTEM`).
    """
    print('- Version of the tool:', TOOL_VERSION)
    print('- Version of Python:', PYTHON_VERSION)
    print('- Operating system:', OPERATING_SYSTEM + '\n')
