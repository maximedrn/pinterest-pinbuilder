# -*- coding: utf-8 -*-
# app/utils/logger/console_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from sys import exc_info
from traceback import format_exception_only
from typing import Dict, List

from app.constants.colors import GREEN, RED, YELLOW
from app.utils.logger.logger_manager import Logger, LoggerManager


class Console(LoggerManager):
    """A class for managing console output, including error, informational,
    and success messages with optional titles. It extends the LoggerManager
    class for logging functionality.

    Methods:
    --------
        __init__(self, file_name: str, title: str | None = None) -> None:
            Initialize the Console instance with a log file and an
            optional title.

        set_title(self, title: str) -> None:
            Set or update the title for the console output.

        error(self, message: str) -> None:
            Display an error message in the console and log any
            associated error.

        info(self, message: str, second_message: str | None = None) -> None:
            Display an informational message in the console with optional
            second message.

        success(self, message: str,
                second_message: str | None = None) -> None:
            Display a success message in the console with optional
            second message.

        message(self, message: str, second_message: str | None = None) -> None:
            Display a general console message with optional second message.
    
    Private methods:
    ----------------
        __console(
                self, message: str, second_message: str | None = None,
                color: str | None = None) -> None:
            Display a console message with a title, main message,
            optional second message, and color.
    """
    
    def __init__(self, file_name: str, title: str | None = None) -> None:
        """Initialize the Console instance with a log file and an
        optional title.

        Parameters:
        -----------
            file_name (str): The name of the log file to use for storing 
                console output.
            title (str | None, optional): An optional title for the 
                console output. Defaults to None.
        """
        self.__title: str | None = title
        super().__init__(file_name)
        
    def set_title(self, title: str) -> None:
        """Set or update the title for the console output.

        Parameters:
        -----------
            title (str): The title to be displayed in the console output.
        """
        self.__title: str | None = title

    def __console(self, message: str, second_message: str | None = None,
                    color: str | None = None) -> None:
        """Display a console message with a title, main message, optional
        second message, and color.

        Parameters:
        -----------
            message (str): The main message to display in the console.
            second_message (str | None, optional): An optional second message.
                Defaults to None.
            color (str | None, optional): The color of the console message.
                Defaults to None.
        """
        content: Dict[str, str] = self._format_content(
            title=self.__title, message=message,
            second_message=second_message, color=color)
        self._write_file(self._update_content(content))
        
    def error(self, message: str) -> None:
        """Display an error message in the console and log any
        associated error.

        Parameters:
        -----------
            message (str): The error message to display in the console.
        """
        exc_type, exc_value, _ = exc_info()
        traceback: List[str] = format_exception_only(exc_type, exc_value)
        second_message: str = traceback[0]
        Logger.error()
        self.__console(message, second_message, RED)

    def info(self, message: str, second_message: str | None = None) -> None:
        """Display an informational message in the console with optional
        second message.

        Parameters:
        -----------
            message (str): The information message to display in the console.
            second_message (str | None, optional): An optional second message.
                Defaults to None.
        """
        self.__console(message, second_message, YELLOW)
        
    def success(self, message: str,
                second_message: str | None = None) -> None:
        """Display a success message in the console with optional
        second message.

        Parameters:
        -----------
            message (str): The success message to display in the console.
            second_message (str | None, optional): An optional second message.
                Defaults to None.
        """
        self.__console(message, second_message, GREEN)
        
    def message(self, message: str,
                second_message: str | None = None) -> None:
        """Display a general console message with optional second message.

        Parameters:
        -----------
            message (str): The general message to display in the console.
            second_message (str | None, optional): An optional second message.
                Defaults to None.
        """
        self.__console(message, second_message)
