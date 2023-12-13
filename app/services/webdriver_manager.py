# -*- coding: utf-8 -*-
# app/services/webdriver_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from multiprocessing.managers import DictProxy
from os import system
from os.path import exists
from typing import Any

from selenium.webdriver import ChromeOptions
from undetected_chromedriver import Chrome, Patcher
from webdriver_manager.chrome import ChromeDriverManager as CDM
from webdriver_manager.core.driver_cache import DriverCacheManager as DCM
from webdriver_manager.core.os_manager import (
    ChromeType, OperationSystemManager as OSM)

from app.constants.messages import (
    WEBDRIVER, WEBDRIVER_DOWNLOAD, WEBDRIVER_DOWNLOAD_ERROR,
    WEBDRIVER_DOWNLOADED, WEBDRIVER_NOT_PATCHED, WEBDRIVER_PATCHED,
    WEBDRIVER_PATCHING, WEBDRIVER_PATH_SET, WEBDRIVER_SIGNED, WEBDRIVER_SIGNING, WEBDRIVER_SIGNING_ERROR)
from app.constants.paths import ASSETS_FOLDER, WEBDRIVER_FILE
from app.constants.processes import MANAGER_PROCESSES, LOGIN_PROCESS
from app.constants.version import MACOS, OPERATING_SYSTEM_ALT
from app.constants.webdriver import (
    CHROME_OPTIONS, CODE_SIGN_SIGN, CODE_SIGN_UNSIGN)
from app.utils.exceptions import WebdriverDownloadError, WebdriverPatchError
from app.utils.logger.console_manager import Console
from app.utils.pid_manager import save_processes


class WebdriverManager:
    """A class for managing webdrivers.

    This class provides methods to download, patch, and configure webdrivers.

    Methods:
    --------
        open_webdriver(self) -> Webdriver:
            Download, patch and open the webdriver.

        close_webdriver(self) -> None:
            Close the webdriver if it is running.
            
    Private methods:
    ----------------
        ___get_chrome_version(self) -> int:
            Get the major version of Google Chrome.

        __patch_webdriver(self) -> None:
            Patch the webdriver if necessary.

        __download_webdriver(self) -> bool:
            Download the webdriver if not already available.

        __set_up_new_webdriver(self) -> None:
            Set up a new webdriver with configured options.

    Attributes:
    -----------
        __chrome_version (int): The major version of Google Chrome.
        __console (Console): The `Console` instance for logs.
    """
    
    def __init__(self) -> None:
        """Initializes the Webdriver class."""
        self.__chrome_version: int = self.__get_chrome_version()
        self.__console: Console = Console(LOGIN_PROCESS, WEBDRIVER)
    
    def __get_chrome_version(self) -> int:
        """Get the major version of Google Chrome.
        
        Returns:
        --------
            int: The major version of Google Chrome.
        """
        __version: str | None = OSM().get_browser_version_from_os(
            ChromeType.GOOGLE)  # Get the current Chrome version.
        return int(__version.split('.')[0]) if __version else 110
    
    def __download_webdriver(self) -> bool:
        """Download the webdriver if not already available.

        Returns:
        --------
            bool: True if the download succeed, otherwise False.
        """
        try:  # Attempt to download the webdriver using the `CDM()` class.
            self.__console.message(WEBDRIVER_DOWNLOAD)
            self.__browser_path: str = CDM(  # CDM downloads the webdriver.
                cache_manager=DCM(root_dir=ASSETS_FOLDER)).install()
            self.__console.success(WEBDRIVER_DOWNLOADED)
        except (Exception, WebdriverDownloadError):
            # If an error occurs during webdriver download, handle the error.
            if not exists(WEBDRIVER_FILE):  # Check if a webdriver file exists.
                self.__console.error(WEBDRIVER_DOWNLOAD_ERROR)
                return False  # Return False to indicate that download failed.
            self.__console.success(WEBDRIVER_PATH_SET)
            self.__browser_path: str = WEBDRIVER_FILE
        return True  # The webdriver file has been downloaded or found.
    
    def __patch_webdriver(self) -> None:
        """Patch the webdriver if necessary."""
        self.__console.message(WEBDRIVER_PATCHING)
        try:  # Attempt to patch the webdriver using the `uc.Patcher()` class.
            Patcher(self.__browser_path, False, self.__chrome_version).auto()
            self.__console.success(WEBDRIVER_PATCHED)
        except (WebdriverPatchError, Exception):
            # In case of an error, log an error message with error
            # details and indicate that webdriver patching failed.
            self.__console.error(WEBDRIVER_NOT_PATCHED)
    
    def __sign_webdriver(self) -> None:
        """Re-sign the webdriver on macOS."""
        try:  # Attempt to re-sign the webdriver after the patch.
            self.__console.message(WEBDRIVER_SIGNING)
            system(CODE_SIGN_UNSIGN.format(self.__browser_path))
            system(CODE_SIGN_SIGN.format(self.__browser_path))
            self.__console.message(WEBDRIVER_SIGNED)
        except Exception:
            self.__console.error(WEBDRIVER_SIGNING_ERROR)
    
    def __set_up_new_webdriver(self, manager: DictProxy[Any, Any]) -> None:
        """Set up a new webdriver with configured options."""
        # Create a ChromeOptions object to configure Chrome browser options.
        chrome_options: ChromeOptions = ChromeOptions()
        for option in CHROME_OPTIONS:  # Add specified Chrome options from
            chrome_options.add_argument(option)  # the CHROME_OPTIONS list.
        self.driver: Chrome = Chrome(  # Initialize the Chrome webdriver.
            log_level=0, driver_executable_path=self.__browser_path,
            options=chrome_options, version_main=self.__chrome_version)
        self.driver.maximize_window()  # Maximize the browser window
        manager[MANAGER_PROCESSES] = save_processes(self.driver)

    def open_webdriver(self, manager: DictProxy[Any, Any]) -> None:
        """Download, patch and open the webdriver."""
        if not self.__download_webdriver():  # Download the webdriver.
            raise WebdriverDownloadError()
        self.__patch_webdriver()  # Patch the webdriver.
        if OPERATING_SYSTEM_ALT == MACOS:
            self.__sign_webdriver()  # Re-sign the webdriver on macOS.
        self.__set_up_new_webdriver(manager)  # Set up a new webdriver.
    
    def close_webdriver(self) -> None:
        """Close the webdriver if it is running."""
        try:  # Try to close the webdriver.
            if isinstance(self.driver, Chrome):
                self.driver.quit()
        except Exception:  # The webdriver is closed,
            pass  # or no webdriver is started.
