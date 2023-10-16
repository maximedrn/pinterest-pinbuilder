# -*- coding: utf-8 -*-
# app/common/file_reader.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from json import loads
from os.path import exists
from typing import Any, Dict, List, Tuple


class FileReader:
    """This class provides file reading functionality.
        
    Private methods:
    ----------------
        __retrieve_file_content(self) -> Tuple[List[Dict[str, Any]], int]:
            Retrieve and load the content of the data file.

    Attributes:
    -----------
        file_path (str): The path to the data file.
        file_content (List[Dict[str, Any]]): The content of the data file.
        file_length (int): The length of the data file content.
    """
    
    def __init__(self, file_path: str) -> None:
        """Initialize a FileReader instance with the specified data file.

        Parameters:
        -----------
            file_path (str): The path to the data file.
        """
        self.file_path: str = file_path
        self.file_content, self.file_length = self.__retrieve_file_content()
        
    def __retrieve_file_content(self) -> Tuple[List[Dict[str, Any]], int]:
        """Retrieve and load the content of the data file.

        Returns:
        --------
            Tuple[List[Dict[str, Any]], int]:
                A tuple containing the file content and its length.
        """
        if not exists(self.file_path):  # The file does not exist.
            return [], 0  # Return the content of an empty file.
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content: List[Dict[str, Any]] = loads(file.read())
        return content, len(content)
