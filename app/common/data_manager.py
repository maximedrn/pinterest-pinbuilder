# -*- coding: utf-8 -*-
# app/common/data_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from copy import deepcopy
from typing import Any, Dict, List, Union

from app.common.data_checker import DataChecker
from app.common.file_manager import FileManager
from app.constants.file_settings import UPLOAD_DATA
from app.constants.messages import DATA_FORMAT_ERROR
from app.utils.exceptions import DataFormatError


class DataManager(FileManager):
    """This class combines file management and data validation features.

    Methods:
    --------
        verify_content(index: int) -> bool:
            Retrieve and verify data content from the specified index.

        retrieve_content() -> Dict[str, Any]:
            Retrieve current loaded data.
            
        __getitem__(key: str) -> Any:
            Retrieve the value according to the key of the current
            loaded data.
            
    Private methods:
    ----------------
        __check_content_integrity(data: Dict[str, Any]) -> None:
            Check the integrity of the data content.

    Attributes:
    -----------
        FileData (Union[str, int, float, List[Dict[str, Any]]]):
            The expected data type for retrieved data.
    """

    FileData = Union[str, int, float, List[Dict[str, Any]]]
    
    def __init__(self, file_path: str, delete_temp_file: bool) -> None:
        """Initialize a DataManager instance with the specified data file.

        Parameters:
        -----------
            file_path (str): The path to the data file.
            delete_temp_file (bool): Let the process start from scratch
                with the selected file, or continue where it left off.
        """
        FileManager.__init__(self, file_path, delete_temp_file)
        
    def __check_content_integrity(self, data: Dict[str, Any]) -> None:
        """Check the integrity of the data content.
        
        Parameters:
        -----------
            data (Dict[str, Any]): The current loaded data to verify.

        Raises:
        -------
            DataFormatError: If the data content format is invalid.
        """
        if not any(key in data for key in UPLOAD_DATA):
            raise DataFormatError(DATA_FORMAT_ERROR)
        
    def verify_content(self, index: int) -> bool:
        """Retrieve data content from the specified index.
        
        It checks for its integrity by performing data validation.

        Parameters:
        -----------
            index (int): The index of the data content to retrieve.
            
        Returns:
        --------
            bool: True if the values of the current data are correct;
            otherwise False.
        """
        self.__current_data: Dict[str, Any] = self.file_content[index]
        self.__check_content_integrity(self.__current_data)
        return DataChecker(self.__current_data)()
        
    def retrieve_content(self) -> Dict[str, Any]:
        """Retrieve current loaded data.
        
        Add the missing keys to the loaded data if they are missing.
        Initialize the values to None.

        Returns:
        --------
            Any: The retrieved data by index.
        """
        # Create a dictionary from the upload data keys.
        upload_data_to_dict: Dict[str, Any] = dict.fromkeys(UPLOAD_DATA)
        # Copy the current loaded data and add the existing key/value if
        # they are not empty. Otherwise it is set to None.
        __current_data: Dict[str, Any] = deepcopy(self.__current_data)
        [upload_data_to_dict.update({key: value})
         for key, value in __current_data.items() if value]
        return upload_data_to_dict
    
    def __getitem__(self, key: str) -> Any:
        """Retrieve the value according to the key of the current loaded data.

        Parameters:
        -----------
            key (str): The key of the current loaded data.

        Returns:
        --------
            Any: The value associated to this key.
        """
        return self.__current_data[key] \
            if key in self.__current_data else None
