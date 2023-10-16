# -*- coding: utf-8 -*-
# app/common/file_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from datetime import datetime as dt
from json import loads
from os.path import basename, dirname, exists, join
from pathlib import Path
from shutil import copy2
from typing import Any, Dict, List
from uuid import uuid4

from app.common.file_reader import FileReader
from app.common.file_writer import FileWriter
from app.constants.file_settings import US_DATETIME_FORMAT
from app.constants.messages import INTERNAL, TEMP_REMOVE_ERROR
from app.constants.paths import TEMP_FOLDER
from app.constants.processes import UPLOAD_PROCESS
from app.utils.exceptions import TempFileError
from app.utils.logger.console_manager import Console


class FileManager(FileReader):
    """This class provides temporary file management features.

    Methods:
    --------
        generate_name_for_file() -> str:
            Generate a unique name for a file based on the current datetime.
    
        remove_element_from_file(self, index: int) -> None:
            Remove an element from the temporary file.

        check_temporary_file_content(self) -> bool:
            Check if the temporary file contains content.

        delete_temporary_file(self) -> None:
            Delete the temporary file if it exists.
    
    Private methods:
    ----------------
        __create_temporary_file(self) -> None:
            Create a temporary file if it does not exist.

    Attributes:
    -----------
        __temp_folder (str): The path to the temporary folder.
        __temp_file (str): The path to the temporary file.
        __remove_element_attempt (int): Counter for
            `remove_element_from_file()` attempts.
            
    """
    
    Content = Dict[str, List[Dict[str, Any]]]
    
    def __init__(self, file_path: str, delete_temp_file: bool) -> None:
        """Initialize a FileManager instance with the specified data file.

        Parameters:
        -----------
            file_path (str): The path to the data file.
            delete_temp_file (bool): Let the process start from scratch
                with the selected file, or continue where it left off.
        """
        super().__init__(file_path)
        __file_folder: str = dirname(self.file_path)
        __file_name: str = basename(self.file_path)
        self.__temp_folder: str = join(__file_folder, TEMP_FOLDER)
        self.__temp_file: str = join(self.__temp_folder, __file_name)
        self.__remove_element_attempt: int = 0
        self.__create_temporary_file(delete_temp_file)
        
    def __create_temporary_file(self, delete_temp_file: bool) -> None:
        """Create a temporary file if it does not exist.
        
        It copies the initial file into the temporary folder
        if it is not already done.
        
        Parameters:
        -----------
            delete_temp_file (bool): Let the process start from scratch
                with the selected file, or continue where it left off.
        """
        Path(self.__temp_folder).mkdir(parents=True, exist_ok=True)
        # Copy the initial file if it is not present in the temporary folder.
        if not exists(self.__temp_file) or delete_temp_file:
            copy2(self.file_path, self.__temp_file)
            
    @staticmethod
    def generate_name_for_file() -> str:
        """Generate a unique name for a file based on the current datetime.

        Returns:
        --------
            str: A unique file name in the format
                "YYYY-MM-DD_HH-MM-SS_xxxx.json", where "xxxx"
                represents the first 4 characters of a random UUID.

        Example:
        --------
            >>> FileManager.generate_name_for_file()
            '2023-09-14_15-30-45_abcd.json'
        """
        __current_datetime: str = dt.now().strftime(US_DATETIME_FORMAT)
        return __current_datetime + '_' + str(uuid4())[:4] + '.json'
    
    def remove_element_from_file(self, index: int) -> None:
        """Remove an element from the temporary file.

        Parameters:
        -----------
            index (int): The index of the element to remove
                + the starting value.
        """
        try:  # Attempt to remove the item from the temporary file.
            file_reader: FileReader = FileReader(self.__temp_file)
            temp_file_length: int = file_reader.file_length
            temp_file_content: List[Dict[str, Any]] = file_reader.file_content
            if temp_file_content:  # Prevent an error in case of an
                temp_file_content.pop(  # empty file.
                    self.file_length - temp_file_length - index)
            FileWriter.write_content(self.__temp_file, temp_file_content)
        except (Exception, TempFileError):
            if self.__remove_element_attempt < 2:
                self.__remove_element_attempt += 1
                return self.remove_element_from_file(index)
            Console(UPLOAD_PROCESS, INTERNAL).error(TEMP_REMOVE_ERROR)
            self.__remove_element_attempt: int = 0
    
    def check_temporary_file_content(self) -> bool:
        """Check if the temporary file contains content.

        Returns:
        --------
            bool: True if the temporary file exists and has
                content, otherwise False.
        """
        if not exists(self.__temp_file):
            return False  # The temporary file does not exist.
        with open(self.__temp_file, 'r', encoding='utf-8') as file:
            content: FileManager.Content = loads(file.read())
        return bool(content)
    
    def delete_temporary_file(self) -> None:
        """Delete the temporary file if it exists."""
        Path(self.__temp_folder).unlink(missing_ok=True)
