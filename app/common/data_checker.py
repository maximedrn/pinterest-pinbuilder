# -*- coding: utf-8 -*-
# app/common/data_checker.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from datetime import datetime as dt, timedelta
from pathlib import Path
from re import match
from typing import Any, Dict, List

from validators.url import pattern

from app.constants.file_settings import (
    DATA_LENGTH, DATETIME, DATETIME_FORMAT,
    DATETIME_FORMAT_REGEX, DATETIME_SCHEDULE_LIMIT, FILE_PATH, LINK,
    PAID_PIN, PINBOARD, TOPIC_TAGS, TOPIC_TAGS_KEYS)
from app.constants.messages import (
    DATA_CHECKER_ERROR, DATETIME_FORMAT_ERROR, DATETIME_PAST_ERROR,
    DATETIME_SCHEDULE_ERROR, EXTERNAL_LINK_ERROR, FILE_PATH_ERROR,
    FILE_PATH_VALUE_ERROR, PIN, PINBOARD_VALUE_ERROR,
    STRING_LENGTH_ERROR, TOPIC_TAGS_ERROR)
from app.constants.processes import UPLOAD_PROCESS
from app.utils.exceptions import IncorrectValueError, RequiredValueError
from app.utils.logger.console_manager import Console


class DataChecker:
    """This class provides methods to perform data validation and checks.

    Methods:
    --------
        __call__(self, index: int, file_length: int) -> bool:
            Perform all data checks.
            
    Private methods:
    ----------------
        __missing(self, key: str) -> bool:
            Check wether a key is missing or not in the current data.
    
        __check_file_path(self) -> None:
            Check if the "file_path" field.

        __check_string_length(self) -> None:
            Check the length of string values.
        
        __check_pinboard(self) -> None:
            Check if the "pinboard" field.

        __check_external_link(self) -> None:
            Check if an external link is valid (if provided).
            
        __check_topic_tags(self) -> None:
            Check if all the topic tags are valid.

        __check_datetime(self) -> None:
            Check the format and validity of a datetime value.

    Attributes:
    -----------
        __current_data (Dict[str, Any]): The current data to be checked.
    """
    
    def __init__(self, current_data: Dict[str, Any]) -> None:
        """Initialize a DataChecker instance with the provided data.

        Parameters:
        -----------
            current_data (Dict[str, Any]): The current data to be checked.
        """
        self.__current_data: Dict[str, Any] = current_data
        
    def __missing(self, key: str) -> bool:
        """Check wether a key is missing or not in the current data.
        
        Parameters:
        -----------
            key (str): The key to search for in the current data.
            
        Returns:
        --------
            bool: True if the key is missing; otherwise False.
        """
        return key not in self.__current_data
    
    def __check_file_path(self) -> None:
        """Check if the "file_path" field.
        
        Check if it is provided and points to an existing file.

        Raises:
        -------
            RequiredValueError: If "file_path" is missing.
            OSError: If "file_path" does not point to an existing file.
        """
        if self.__missing(FILE_PATH) or not self.__current_data[FILE_PATH]:
            raise RequiredValueError(FILE_PATH_VALUE_ERROR)
        if not Path(self.__current_data[FILE_PATH]).is_file():
            raise OSError(FILE_PATH_ERROR)

    def __check_string_length(self) -> None:
        """Check the length of string values.
        
        Check if it according to the predefined maximum lengths.

        Raises:
        -------
            IncorrectValueError: If any string value
                exceeds the maximum length.
        """
        for key_name, max_length in DATA_LENGTH.items():
            value: str = self.__current_data[key_name] \
                if not self.__missing(key_name) else ''
            if value and len(value) > max_length:
                raise IncorrectValueError(STRING_LENGTH_ERROR.format(
                    key_name=key_name, max_length=max_length))
                
    def __check_pinboard(self) -> None:
        """Check if the "pinboard" field.
        
        Check if the Pinboard is provided for a paid Pin.

        Raises:
        -------
            RequiredValueError: If "pinboard" is missing.
        """
        __is_paid: bool = bool(self.__current_data[PAID_PIN]) \
            if not self.__missing(PAID_PIN) else False
        if __is_paid and not self.__current_data[PINBOARD]:
            raise RequiredValueError(PINBOARD_VALUE_ERROR)

    def __check_external_link(self) -> None:
        """Check if an external link is valid (if provided).

        Raises:
        -------
            IncorrectValueError: If the external link is not a valid URL.
        """
        external_link: str = self.__current_data[LINK] \
            if not self.__missing(LINK) else ''
        if external_link and not pattern.match(external_link):
            raise IncorrectValueError(EXTERNAL_LINK_ERROR)
    
    def __check_topic_tags(self) -> None:
        """Check if all the topic tags are valid.

        Raises:
        -------
            IncorrectValueError: If one of the topic tags is not valid.
        """
        topic_tags: List[Dict[str, str]] = self.__current_data[TOPIC_TAGS] \
            if not self.__missing(TOPIC_TAGS) else []
        for topic_tag in topic_tags:
            if any(key not in topic_tag for key in TOPIC_TAGS_KEYS):
                raise IncorrectValueError(TOPIC_TAGS_ERROR)
    
    def __check_datetime(self) -> None:
        """Check the format and validity of a datetime value.

        Raises:
        -------
            IncorrectValueError: If the datetime format is invalid
                or outside the allowed range.
        """
        __datetime_string: str = self.__current_data[DATETIME] \
            if not self.__missing(DATETIME) else ''
        if not __datetime_string:  # The datetime has not been specified.
            return  # So there's no mistake: the data is optional.
        if not match(DATETIME_FORMAT_REGEX, __datetime_string):
            raise IncorrectValueError(DATETIME_FORMAT_ERROR)
        __datetime: dt = dt.strptime(__datetime_string, DATETIME_FORMAT)
        if __datetime < dt.now():  # Scheduled in the past.
            raise IncorrectValueError(DATETIME_PAST_ERROR)
        if __datetime - dt.now() > timedelta(days=DATETIME_SCHEDULE_LIMIT):
            raise IncorrectValueError(DATETIME_SCHEDULE_ERROR)
        # if __datetime.minute not in (0, 30):
        #     raise IncorrectValueError(DATETIME_MINUTES_ERROR)
        
    def __call__(self, index: int, file_length: int) -> bool:
        """Perform all data checks.
        
        Parameters:
        -----------
            index (int): The index of the data content to verify.
            file_length (int): The selected file length.
        
        Returns:
        --------
            bool: True if all checks pass, otherwise False.
        """
        try: # Each test can result in an exception.
            self.__check_file_path()
            self.__check_string_length()
            self.__check_pinboard()
            self.__check_external_link()
            self.__check_topic_tags()
            self.__check_datetime()
            return True  # All tests have been passed.
        except (RequiredValueError, IncorrectValueError, Exception):
            __title: str = PIN.format(index + 1, file_length)
            Console(UPLOAD_PROCESS, __title).error(DATA_CHECKER_ERROR)
            return False  # An error occurred during verification.
