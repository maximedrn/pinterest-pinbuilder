# -*- coding: utf-8 -*-
# app/services/create/create_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from copy import deepcopy
from datetime import datetime as dt, timedelta
from os.path import join
from re import match
from typing import Any, Dict, List

from app.common.file_manager import FileManager
from app.common.file_writer import FileWriter
from app.constants.file_settings import (
    DATETIME, DATETIME_FORMAT, JS_DATETIME_FORMAT_REGEX, FILE_PATH,
    JS_DATETIME_FORMAT, LINK, LINK_DEFAULT_VALUE, PINBOARD, UPLOAD_DATA)
from app.constants.messages import SAVE_ERROR, SAVE_MESSAGE
from app.constants.paths import UPLOAD_FOLDER
from app.constants.processes import CREATE_PROCESS
from app.constants.webdriver import PINTEREST_URL
from app.services.create.assets_manager import AssetsManager
from app.utils.exceptions import SaveFileError
from app.utils.logger.snackbar_manager import Snackbar


class CreateManager(FileWriter):
    """CreateManager class for managing pin creation and data storage.

    This class provides methods for creating pins, managing data chunks,
    applying data to pins, saving pin data to a file, and checking when
    the data was last saved.

    Methods:
    --------
        __init__(self, assets_folder: str) -> None:
            Initialize the CreateManager with assets and
            file-related settings.

        __getitem__(self, index: int) -> Dict[str, Any]:
            Retrieve a pin dictionary by index from the loaded data.

        get_assets_preview_binary(self) -> List[str]:
            Get binary data representations of asset previews
            for the current chunk.

        load_next_chunk(self) -> bool:
            Load the next data chunk if available.

        load_previous_chunk(self) -> bool:
            Load the previous data chunk if available.

        apply_for_all(self, key_name: str, value: str) -> None:
            Apply a specific value to all pins.

        apply_data_by_index(
                self, index: int, data_from_frontend: Dict[str, Any]) -> None:
            Apply data from the frontend to a specific pin.

        save_file(self) -> None:
            Save the pin data to a file.
            
    Private methods:
    ----------------
        __check_last_time_saved(self) -> None:
            Check if it's time to save the pin data to a file.

    Attributes:
    -----------
        __pins_data (List[Dict[str, Any]]): A list of dictionaries
            representing pin data.
        __upload_file (str): The path to the file where pin data
            will be saved.
        __last_time_saved (datetime): The timestamp when the data
            was last saved.
        __chunk_size (int): The size of each data chunk.
        __loaded_part (int): The index of the currently loaded data chunk.
    """
    
    def __init__(self, assets_folder: str) -> None:
        """Initialize the CreateManager with assets and file-related settings.

        Parameters:
        -----------
            assets_folder (str): The folder containing asset files.
        """
        self.__pins_data: List[Dict[str, Any]] = \
            AssetsManager.retrieve_assets_file(assets_folder)
        self.__upload_file: str = join(
            UPLOAD_FOLDER, FileManager.generate_name_for_file())
        self.__last_time_saved: dt = dt.now()
        self.__chunk_size: int = 32
        self.__loaded_part: int = 0
    
    def __set_default_values(self, pin_data: Dict[str, Any]) -> None:
        if not pin_data[PINBOARD]:
            pin_data[PINBOARD] = PINTEREST_URL
        if not pin_data[LINK]:
            pin_data[LINK] = LINK_DEFAULT_VALUE
    
    def __getitem__(self, index: int) -> Dict[str, Any]:
        """Retrieve a pin dictionary by index from the loaded data.

        Parameters:
        -----------
            index (int): The index of the pin data to retrieve.

        Returns:
        --------
            Dict[str, Any]: The pin data as a dictionary.
        """
        __index: int = self.__chunk_size * self.__loaded_part + index
        __pin_data: Dict[str, Any] = deepcopy(self.__pins_data[__index])
        # Add the missing keys and an empty string as default value
        [__pin_data.update({key: ''})  # to the current selected data.
         for key in UPLOAD_DATA if key not in __pin_data]
        self.__set_default_values(__pin_data)
        return __pin_data

    def get_assets_preview_binary(self) -> List[str]:
        """Get binary data representations of asset previews
        for the current chunk.

        Returns:
        --------
            List[str]: A list of binary data strings.
        """
        __min_index: int = self.__chunk_size * self.__loaded_part
        __max_index: int = min(__min_index + self.__chunk_size, len(
            self.__pins_data))  # Prevent IndexError.
        return [AssetsManager.get_asset_binary(self.__pins_data[index][
            FILE_PATH]) for index in range(__min_index, __max_index)]
            
    def load_next_chunk(self) -> bool:
        """Load the next data chunk if available.

        Returns:
        --------
            bool: True if the next chunk was loaded, False otherwise.
        """
        __next_chunk: int = self.__chunk_size * (self.__loaded_part + 1)
        limit_not_reached: bool = len(self.__pins_data) >= __next_chunk
        self.__loaded_part += bool(limit_not_reached)  # Add 1 or nothing.
        return limit_not_reached
    
    def load_previous_chunk(self) -> bool:
        """Load the previous data chunk if available.

        Returns:
        --------
            bool: True if the previous chunk was loaded, False otherwise.
        """
        previous_chunk_can_be_loaded: bool = self.__loaded_part > 0
        self.__loaded_part: int = max(0, self.__loaded_part - 1)
        return previous_chunk_can_be_loaded
    
    def apply_for_all(self, key_name: str, value: str) -> None:
        """Apply a specific value to all pins.

        Parameters:
        -----------
            key_name (str): The key name for the value to apply.
            value (str): The value to apply to all pins.
        """
        [pin.update({key_name: value}) for pin in self.__pins_data]
        self.__check_last_time_saved()
        
    def apply_data_by_index(
            self, index: int, data_from_frontend: Dict[str, Any]) -> None:
        """Apply data from the frontend to a specific pin.

        Parameters:
        -----------
            index (int): The index of the pin to apply data to.
            data_from_frontend (Dict[str, Any]): Data from the frontend 
                to apply to the pin.
        """
        self.__pins_data[index].update(data_from_frontend)
        self.__check_last_time_saved()
            
    def __convert_pin_data(self) -> List[Dict[str, Any]]:
        """Convert and format pin data for saving.

        Returns:
        --------
            List[Dict[str, Any]]: The formatted pin data.
        """
        __pins_data_copy: List[Dict[str, str]] = deepcopy(self.__pins_data)
        for pin in __pins_data_copy:
            if PINBOARD in pin and pin[PINBOARD] == PINTEREST_URL: 
                pin[PINBOARD] = ''  # Remove the default Pinboard URL.
            if LINK in pin and pin[LINK] == LINK_DEFAULT_VALUE:
                pin[LINK] = ''  # Remove the default external URL.
            if DATETIME not in pin or not pin[DATETIME]:  # The datetime
                continue  # value does not exist or has not been specified.
            if not match(JS_DATETIME_FORMAT_REGEX, pin[DATETIME]):
                continue  # The datetime is not empty but wrongly formatted.
            __datetime: dt = dt.strptime(pin[DATETIME], JS_DATETIME_FORMAT)
            pin[DATETIME] = __datetime.strftime(DATETIME_FORMAT)
        return __pins_data_copy
            
    def save_file(self) -> None:
        """Save the pin data to a file.

        Raises:
        -------
            SaveFileError: If there is an error while saving the file.
        """
        try:  # Try to save the current file using FileWriter.
            __content: List[Dict[str, Any]] = self.__convert_pin_data()
            self.write_content(self.__upload_file, __content)
            self.__last_time_saved: dt = dt.now()
            Snackbar(CREATE_PROCESS).success(
                SAVE_MESSAGE.format(self.__upload_file))
        except (Exception, SaveFileError):
            Snackbar(CREATE_PROCESS).error(SAVE_ERROR)
    
    def __check_last_time_saved(self) -> None:
        """Check if it's time to save the pin data to a file.

        If the time elapsed since the last save is greater than 20 seconds,
        the data will be saved to a file.
        """
        if dt.now() - self.__last_time_saved > timedelta(seconds=20):
            self.save_file()  # Each time the data is updated.
