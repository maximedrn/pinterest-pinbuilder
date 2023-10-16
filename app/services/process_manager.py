# -*- coding: utf-8 -*-
# app/services/process_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from multiprocessing import Process
from multiprocessing.managers import DictProxy
from typing import Any, Dict

from app.constants.file_settings import (
    DELETE_TEMP_FILE, FILE_PATH, MAXIMUM_ATTEMPTS, STARTING_VALUE)
from app.constants.webdriver import UUID
from app.services.login.cookie_manager import CookieManager
from app.services.login.login_process import LoginProcess
from app.services.login.user_manager import UserManager
from app.services.upload.upload_process import UploadProcess
from app.utils.logger.console_manager import Console
from app.utils.pid_manager import kill_processes


class ProcessManager(UserManager, CookieManager):
    """ProcessManager class for managing upload processes and login
    processes in a multiprocessing environment.

    This class extends the functionality of both UserManager and
    CookieManager to facilitate the management of upload processes
    and login processes. It provides methods for starting and stopping
    upload processes, starting a login process, and managing retrieved
    cookies.

    Methods:
    --------
        __init__(self, manager: DictProxy) -> None:
            Initialize a CookieManager instance.

        start_upload_process(self, **kwargs: Dict[str, Any]) -> bool:
            Start an upload process with the provided keyword arguments.

        start_login_process(self) -> bool:
            Start the login process as a separate thread.

        stop_process(self, log_file_name: str) -> None:
            Terminate the currently running process and clear the
            associated log.

    Private methods:
    ----------------
        __manage_retrieved_cookies(self, uuid: str) -> Dict[str, Any]:
            Manage retrieved cookies for a specified UUID.

        __int(self, value: Any) -> int:
            Convert a value to an integer if possible, or return 0 if
            conversion is not possible.

    Attributes:
    -----------
        __manager (DictProxy[Any, Any]): A multiprocessing manager for
            sharing data and managing cookies.
    """

    def __init__(self, manager: DictProxy) -> None:
        """Initialize a CookieManager instance.

        This method initializes a `CookieManager` instance, which manages
        cookies in a multiprocessing manager (`manager`).

        Parameters:
        -----------
            manager (DictProxy[Any, Any]): A multiprocessing manager for
                sharing data and managing cookies.
        """
        self.__manager: DictProxy[Any, Any] = manager
    
    def __manage_retrieved_cookies(self, uuid: str) -> Dict[str, Any]:
        """Manage retrieved cookies for a specified UUID.

        This method retrieves cookies associated with the provided UUID and
        checks their validity using the `verify_cookies_field` method. If
        the cookies are not valid, it starts the login process and
        recursively manages the cookies until valid cookies are obtained.

        Parameters:
        -----------
            uuid (str): A unique identifier associated with the cookies
                to be managed.

        Returns:
        --------
            Dict[str, Any]: Valid cookies retrieved for the specified UUID.
        """
        __cookies: Dict[str, Any] = self.retrieve_cookies_by_id(uuid)
        if not self.verify_cookies_field(__cookies):
            self.start_login_process()
            return self.__manage_retrieved_cookies(uuid)
        return __cookies
    
    def __int(self, value: Any) -> int:
        """Convert a value to an integer if possible, or return 0 if
        conversion is not possible.

        This method attempts to convert the provided value to an integer
        using `int()`. If the value is not convertible to an integer
        (e.g., if it's not a digit), it returns 0.

        Parameters:
        -----------
            value (Any): The value to be converted to an integer.

        Returns:
        --------
            int: The integer representation of the value, or 0 if
            conversion is not possible.
        """
        return int(value) if str(value).isdigit() else 0
        
    def start_upload_process(self, **kwargs: Dict[str, Any]) -> bool:
        """Start an upload process with the provided keyword arguments.

        Parameters:
        -----------
            **kwargs (Dict[str, Any]): Keyword arguments containing the
                necessary data for the upload process.

        Returns:
        --------
            bool: True if the process was successfully started.
        """
        __uuid: Any = kwargs[UUID]  # Get the account UUID, and
        # retrieve cookies from the file or from a Pinterest login process.
        cookies: Dict[str, Any] =  self.__manage_retrieved_cookies(__uuid)
        # Send the required values used to run the upload process.
        __file_path: str = str(kwargs[FILE_PATH])
        __starting_value: int = self.__int(kwargs[STARTING_VALUE])
        __maximum_attempts: int = self.__int(kwargs[MAXIMUM_ATTEMPTS])
        __delete_temp_file: bool = bool(kwargs[DELETE_TEMP_FILE])
        self.__thread: Process | None = UploadProcess(
            __file_path, __starting_value, __maximum_attempts,
            __delete_temp_file, cookies)()
        return True  # The process is successfully started.
    
    def start_login_process(self) -> bool:
        """Start the login process as a separate thread.

        This method initiates the login process by creating a new
        `LoginProcess` instance with the specified manager and running it
        as a separate thread. It returns `True` to indicate that the
        process has been started.

        Returns:
        --------
            bool: Returns `True` to indicate that the login process has
            been initiated successfully.
        """
        self.__thread: Process | None = LoginProcess(self.__manager)()
        return True
    
    def stop_process(self, log_file_name: str) -> None:
        """Terminate the currently running process and clear the
        associated log.

        This method is used to terminate the currently running process,
        which is typically an upload process. It first checks if the process
        is an instance of `multiprocessing.Process` and uses the built-in
        `terminate()` method to close the process if it is. After terminating
        the process, it sets the thread to `None` and attempts to kill any
        remaining processes associated with the manager.

        Additionally, this method creates a `Console` instance with the
        specified log file name and clears the log to ensure that any
        remaining log data is removed.

        Parameters:
        -----------
            log_file_name (str): The name of the log file used to clear
                associated log data.
        """
        if isinstance(self.__thread, Process):  # Use the built-in
            self.__thread.terminate()  # method to close the process.
        self.__thread: Process | None = None
        kill_processes(self.__manager)
        Console(log_file_name).clear()
