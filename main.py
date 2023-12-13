# -*- coding: utf-8 -*-
# main.py

"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn
"""


from __future__ import annotations
from os import chdir
from os.path import dirname, abspath
from typing import Any, Callable

# NOTE: this code block must not be moved.
from app.utils.func import check_python_version
check_python_version()  # Make sure Python 3.8 or higher is used.
from app.utils.modules_manager import ModulesManager
ModulesManager().install_modules()  # Install required modules.

from eel import _expose, init, start
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

from app.common.screen_manager import get_interface_size
from app.constants.paths import (
    ALLOWED_EXTENSIONS, BROWSER_ARGUMENTS, FRONTEND_BROWSER,
    FRONTEND_FILE, FRONTEND_FOLDER, FRONTEND_HOST, FRONTEND_PORT)
from app.constants.processes import MANAGER_DEFAULT_STATE
from app.interface import Interface
from app.utils.func import cls, display_configuration
from app.utils.pid_manager import kill_listener_processes


chdir(dirname(abspath(__file__)))  # Move to the actual path.
disable_warnings(category=InsecureRequestWarning)

# Init the HTML/CSS interface.
init(FRONTEND_FOLDER, allowed_extensions=ALLOWED_EXTENSIONS)


def main() -> None:
    """Entry point for the program.

    This function serves as the entry point for the program and performs
    various tasks to initialize and start the program's interface. It clears
    command line outputs, displays configuration information, terminates
    conflicting processes, initializes the program's interface, and starts
    the frontend interface.

    Tasks performed by this function:
    1. Clear command line outputs.
    2. Display tool and operating system settings.
    3. Terminate conflicting processes to free up specified ports.
    4. Initialize an instance of the `Interface` class.
    5. Expose non-private callable methods of the `Interface` class.
    6. Set default attributes in the `Interface` class.
    7. Retrieve the size and position for the frontend interface.
    8. Start the frontend interface with specified parameters.
    """
    cls()  # Clear all the command line outputs.
    display_configuration()  # Show the tool and operating system settings.
    kill_listener_processes()  # Kill processes in conflict with the port.

    __interface: Interface = Interface()
    for attribute in dir(__interface):
        # `getattr(Class, "method")` returns the reference of 
        # `Class.method()` and link it to the literal name of the method.
        __is_private_method: bool = attribute.startswith('_')
        __callable: Callable[..., Any] = getattr(__interface, attribute)
        if not __is_private_method and callable(__callable):
            _expose(attribute, __callable)

    for key, value in MANAGER_DEFAULT_STATE.items():
        __interface[key] = value  # `__getitem__()` method.
    
    __frontend_size, __frontend_position = get_interface_size()
    start(  # Start the frontend interface.
        FRONTEND_FILE, host=FRONTEND_HOST, port=FRONTEND_PORT,
        size=__frontend_size, position=__frontend_position, shutdown_delay=10,
        mode=FRONTEND_BROWSER, cmdline_args=BROWSER_ARGUMENTS,
        disable_cache=True)


if __name__ == '__main__':
    main()
