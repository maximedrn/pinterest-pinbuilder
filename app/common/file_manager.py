from __future__ import annotations

from datetime import datetime as dt
from json import loads
from os.path import basename, dirname, exists, join
from pathlib import Path
from shutil import copy2
from typing import Any

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

        add_index_to_file(file_path: str) -> str:
            Append an index to a file path to make it unique.

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

    Content = dict[str, list[dict[str, Any]]]

    def __init__(self, file_path: str, delete_temp_file: bool) -> None:
        """Initialize a FileManager instance with the specified data file.

        Parameters:
        -----------
            file_path (str): The path to the data file.
            delete_temp_file (bool): Let the process start from scratch
                with the selected file, or continue where it left off.
        """
        self.__file_path: str = file_path
        __file_folder: str = dirname(self.__file_path)
        __file_name: str = basename(self.__file_path)
        self.__temp_folder: str = join(__file_folder, TEMP_FOLDER)
        self.__temp_file: str = join(self.__temp_folder, __file_name)
        self.__remove_element_attempt: int = 0
        self.__create_temporary_file(delete_temp_file)
        super().__init__(self.__temp_file)

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
            copy2(self.__file_path, self.__temp_file)

    @staticmethod
    def generate_name_for_file() -> str:
        """Generate a unique name for a file based on the current datetime.

        Returns:
        --------
            str: A unique file name in the  "YYYY-MM-DD HH-MM-SS.json" format.

        Example:
        --------
            >>> FileManager.generate_name_for_file()
            '2023-09-14 15-30-45.json'
        """
        __current_datetime: str = dt.now().strftime(US_DATETIME_FORMAT)
        return __current_datetime + ".json"

    @staticmethod
    def add_index_to_file(file_path: str) -> str:
        """Append an index to a file path to make it unique.

        This method takes a file path and appends an index to the file name to
        ensure that the resulting file path does not already exist. If the
        original file path exists, it keeps incrementing the index until it
        finds a unique file path.

        Parameters:
        -----------
            file_path (str): The original file path to which an index will
                be added.

        Returns:
        --------
            str: A modified file path with an added index to make it unique.
        """
        __file_path: Path = Path(file_path)
        __folder: Path = __file_path.parent
        __file_name: str = __file_path.stem + "_{}" + __file_path.suffix
        index: int = 0  # The index that will be added for the file.
        while Path(__file_path).exists() and (index := index + 1):
            __current_file_name: str = __file_name.format(index)
            __file_path: Path = __folder.joinpath(__current_file_name)
        return str(__file_path.name)

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
            temp_file_content: list[dict[str, Any]] = file_reader.file_content
            # Note: `index` increases but the temp file length decrease.
            # Thus it is required to subtract from `index` the difference
            # between the file length and the temp file length.
            temp_file_content.pop(index - self.file_length + temp_file_length)
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
        with open(self.__temp_file, "r", encoding="utf-8") as file:
            content: FileManager.Content = loads(file.read())
        return bool(content)

    def delete_temporary_file(self) -> None:
        """Delete the temporary file if it exists."""
        Path(self.__temp_folder).unlink(missing_ok=True)
