# -*- coding: utf-8 -*-
# app/utils/logger/logger_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from datetime import datetime as dt
from logging import basicConfig, ERROR, error
from os import makedirs
from os.path import join
from socket import socket, AF_INET, SOCK_STREAM
from traceback import format_exc, print_exc
from typing import Any, Dict, List
from uuid import uuid4

from app.common.file_reader import FileReader
from app.common.file_writer import FileWriter
from app.constants.file_settings import US_DATETIME_FORMAT
from app.constants.paths import LOG_FOLDER, FRONTEND_HOST, FRONTEND_PORT
from app.constants.webdriver import UUID
from app.utils.exceptions import LoggerError


class LoggerManager(FileWriter, FileReader):
    """Manage logging and sending messages to a file and a frontend.

    This class provides methods for writing log messages to a file and 
    sending them to a frontend interface.

    Methods:
    --------
        __init__(self, file_name: str) -> None:
            Initialize a new LoggerManager instance.
            
        clear(self) -> LoggerManager:
            Clear the contents of the log file.
            
    Protected methods:
    ------------------
        _format_content(
                self, message: str, second_message: str | None = None,
                title: str | None = None, color: str | None = None,
                icon: str | None = None) -> Dict[str, Any]:
                
        _write_file(self, content: List[Dict[str, str]]) -> None:
            
    Private methods:
    ----------------
        __create_folder(self) -> None:
            Create the log folder if it does not exist.
            
         __convert(self, message: str) -> str:
            Convert color codes in a log message to HTML tags.

    Attributes:
    -----------
        __file_name (str): The name of the log file.
        __uuid (str): The unique ID for the log message.
    """
    
    def __init__(self, file_name: str) -> None:
        """Initialize a new LoggerManager instance.

        Parameters:
        -----------
            file_name (str): The name of the log file.
        """
        self.__file_name: str = join(LOG_FOLDER, file_name)
        self.__uuid: str = str(uuid4())
        
    def _format_content(
            self, message: str, second_message: str | None = None,
            title: str | None = None, color: str | None = None,
            icon: str | None = None) -> Dict[str, Any]:
        """Format log content into a dictionary for logging.

        This method takes various log-related parameters, such as the main
        message, an optional second message, title, color, and an icon, and
        formats them into a dictionary. This dictionary is suitable for
        logging purposes and typically includes a unique UUID, title, message,
        second message, color, and icon.

        Parameters:
        -----------
            message (str): The main message to be logged.
            second_message (str | None, optional): An optional second message.
                Defaults to None.
            title (str | None, optional): An optional title for the log
                content. Defaults to None.
            color (str | None, optional): The color of the log content.
                Defaults to None.
            icon (str | None, optional): An optional icon associated with the
                log content. Defaults to None.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing formatted log content with
            the specified parameters.
        """
        return {
            UUID: self.__uuid,
            "title": title,
            "message": message,
            "second_message": second_message,
            "color": color,
            "icon": icon
        }
    
    def __create_folder(self) -> None:
        """Create the log folder if it does not exist."""
        makedirs(LOG_FOLDER, exist_ok=True)
        
    def _write_file(self, content: List[Dict[str, str]]) -> None:
        """Write the provided content to a log file, create a folder
        if necessary, and send the log data to a frontend service.

        This method establishes a connection to a frontend service
        specified by `FRONTEND_HOST` and `FRONTEND_PORT` and sends
        the log content. It also creates the `LOG_FOLDER` directory
        if it doesn't exist and logs any exceptions or `LoggerError`
        instances.

        Parameters:
        -----------
            content (List[Dict[str, str]]): A list of dictionaries
                containing log content.

        Raises:
        -------
            LoggerError: If an error occurs while writing to the log file.
        """
        try:
            connection: socket = socket(AF_INET, SOCK_STREAM)
            connection.connect((FRONTEND_HOST, FRONTEND_PORT))
            self.__create_folder()  # Create the `LOG_FOLDER` directory.
            self.write_content(self.__file_name, content)
            connection.close()
        except (Exception, LoggerError):
            Logger.error()

    def __retrieve_file_content(self) -> List[Dict[str, str]]:
        """Retrieve the content of the log file associated with
        the instance.

        This method initializes a `FileReader` instance to read
        the content of the log file and returns it as a list of
        dictionaries.

        Returns:
        --------
            List[Dict[str, str]]: The content of the log file as a list
            of dictionaries.
        """
        FileReader.__init__(self, self.__file_name)
        return self.file_content
    
    def _update_content(
            self, content: Dict[str, str]) -> List[Dict[str, str]]:
        """Update the content of the log file with new log data and
        return the updated content.

        This method retrieves the previous content of the log file
        using `__retrieve_file_content`, and if an entry with the same
        UUID exists, it updates that entry with the provided content.
        If no matching UUID is found, it appends the new content to
        the existing log content.

        Parameters:
        -----------
            content (Dict[str, str]): The log content to be updated or added.

        Returns:
        --------
            List[Dict[str, str]]: The updated content of the log file as a
            list of dictionaries.
        """
        __previous: List[Dict[str, str]] = self.__retrieve_file_content()
        for index, element in enumerate(__previous):
            if element[UUID] == self.__uuid:
                __previous[index] = content
                return __previous
        return __previous + [content]
        
    def clear(self) -> None:
        """Clear the contents of the log file."""
        self.__create_folder()  # Create the `LOG_FOLDER` directory.
        self.write_content(self.__file_name, [])


class Logger:
    """Simple logger for printing error messages to the console.

    This class provides a basic logging method for printing error messages
    to the console in red text.

    Methods:
    --------
        error(self) -> None:
            Print an error message to the console in red text.
    """
        
    @staticmethod
    def error() -> None:
        """Print an error message to the console in red text."""
        __log_file_name: str = dt.now().strftime(US_DATETIME_FORMAT) + '.log'
        __log_file: str = join(LOG_FOLDER, __log_file_name)
        basicConfig(filename=__log_file, level=ERROR)
        error(format_exc())
        print_exc()
