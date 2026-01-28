from os import name, system
from sys import exit as sys_exit
from sys import version_info

from app.constants.colors import COLORAMA_RED, COLORAMA_RESET
from app.constants.messages import PYTHON_VERSION_ERROR
from app.constants.version import (
    OPERATING_SYSTEM,
    PYTHON_VERSION,
)


def cls() -> None:
    """Clear console from the command line.

    It uses the default system function:
        - "cls" if system is Windows.
        - "clear" is system is Linux or MacOS.
    """
    # Type the specific command using the system function.
    # "cls" if operating system is Windows, else "clear".
    system("cls" if name == "nt" else "clear")


def exit(message: str = "") -> None:
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


def display_configuration() -> None:
    """Display the configuration information of the tool.

    This function prints the following information:
        - Version of the tool (`TOOL_VERSION`).
        - Version of Python (`PYTHON_VERSION`).
        - Operating system (`OPERATING_SYSTEM`).
    """
    print("- Version of Python:", PYTHON_VERSION)
    print("- Operating system:", OPERATING_SYSTEM + "\n")
