from __future__ import annotations

from json import loads
from os.path import exists
from typing import Any


class FileReader:
    """This class provides file reading functionality.

    Private methods:
    ----------------
        __retrieve_file_content(self) -> tuple[list[dict[str, Any]], int]:
            Retrieve and load the content of the data file.

    Attributes:
    -----------
        file_path (str): The path to the data file.
        file_content (list[dict[str, Any]]): The content of the data file.
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

    def __retrieve_file_content(self) -> tuple[list[dict[str, Any]], int]:
        """Retrieve and load the content of the data file.

        Returns:
        --------
            tuple[list[dict[str, Any]], int]:
                A tuple containing the file content and its length.
        """
        if not exists(self.file_path):  # The file does not exist.
            return [], 0  # Return the content of an empty file.
        with open(self.file_path, "r", encoding="utf-8") as file:
            content: list[dict[str, Any]] = loads(file.read())
        return content, len(content)
