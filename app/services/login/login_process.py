# -*- coding: utf-8 -*-
# app/services/login/login_process.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from multiprocessing import Process
from multiprocessing.managers import DictProxy
from typing import Any, Callable

from app.services.login.login_manager import LoginManager
from app.services.thread_manager import ThreadManager


class LoginProcess(LoginManager, ThreadManager):
    """LoginProcess class for handling the login process.

    Inherits from LoginManager, UserManager, and ThreadManager
    for login functionality.

    Methods:
    --------
        __init__(self, manager: DictProxy) -> None:
            Initialize a LoginProcess instance with a manager for shared data.
    
        __call__(self) -> Process:
            Initialize and start the login process in a separate thread.

    Attributes:
    -----------
        __manager (DictProxy[Any, Any]): A multiprocessing manager for
            sharing data and managing cookies.
    """
    
    def __init__(self, manager: DictProxy) -> None:
        """Initialize a LoginProcess instance with a manager for shared data.

        Parameters:
        -----------
            manager (DictProxy[Any, Any]): A multiprocessing manager for
                sharing data and managing cookies.
        """
        self.__manager: DictProxy[Any, Any] = manager

    def __call__(self) -> Process:
        """Initialize and start the login process in a separate thread.

        Returns:
        --------
            Process: The running login process thread.
        """
        __login_method: Callable[..., None] = LoginManager().__call__
        return self.run_thread_process(__login_method, args=(self.__manager,))
