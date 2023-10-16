# -*- coding: utf-8 -*-
# app/common/file_writer.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from json import dumps
from typing import Any, Dict, List


class FileWriter:
    """
    FileWriter class for writing content to a JSON file.

    Methods:
    --------
        write_content(file_path: str, content: List[Dict[str, Any]]) -> None:
            Write the provided content to a JSON file.
    """
    
    @staticmethod        
    def write_content(file_path: str, content: List[Dict[str, Any]]) -> None:
        """Write the provided content to a JSON file.

        Parameters:
        -----------
            file_path (str): The path of the JSON file to write.
            content (List[Dict[str, Any]]): The content to write to the file.
        """
        with open(file_path, 'w+', encoding='utf-8') as file:
            file.seek(0)  # Move at the beginning of the file.
            file.truncate(0)  # Remove the content of the file.
            file.write(dumps(content, indent=4))
