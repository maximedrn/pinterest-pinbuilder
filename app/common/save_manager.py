from __future__ import annotations

from json import dumps, loads
from os.path import exists, join
from typing import Any

from app.common.data_manager import DataManager
from app.common.file_manager import FileManager
from app.common.file_writer import FileWriter
from app.constants.file_settings import UPLOAD_DATA
from app.constants.messages import SAVE, SAVE_ERROR, SAVE_MESSAGE
from app.constants.paths import UPLOAD_FOLDER
from app.constants.processes import UPLOAD_PROCESS
from app.utils.exceptions import SaveFileError
from app.utils.logger.console_manager import Console


class SaveManager:
    """This class provides features for saving data related to a new upload.

    Methods:
    --------
        save_upload(self) -> None:
            Save all the details of the Pin for a new upload.

    Private methods:
    ----------------
        __create_save_file(self, data_folder: str) -> None:
            Create a new save file in the specified data folder.

        __save_content(self, data_folder: str, data_keys: list[str]) -> None:
            Save data content to the backup file.

    Attributes:
    -----------
        __file_name (str): The name of the save file.
        data_manager (DataManager): An instance of DataManager
            to retrieve data from.
    """

    def __init__(self, data_manager: DataManager, file_path: str) -> None:
        """Initialize a SaveManager instance with the specified DataManager.

        Parameters:
        -----------
            data_manager (DataManager): An instance of DataManager
                to retrieve data from.
            file_path (str): The path to the file containing data to upload.
        """
        self.__file_name: str = FileManager.add_index_to_file(file_path)
        self.data_manager: DataManager = data_manager

    def __create_save_file(self, data_folder: str) -> None:
        """Create a new save file in the specified data folder.

        Parameters:
        -----------
            data_folder (str): The path to the data folder where
                the save file will be created.
        """
        __save_file: str = join(data_folder, self.__file_name)
        if not exists(__save_file):
            with open(__save_file, "w+", encoding="utf-8") as file:
                file.write(dumps([], indent=4))

    def __save_content(self, data_folder: str, data_keys: list[str]) -> None:
        """Save data content to the backup file.

        Parameters:
        -----------
            data_folder (str): The path to the data folder where
                the save file is located.
            data_keys (list[str]): The keys of the data to save.
        """
        self.__console: Console = Console(UPLOAD_PROCESS, SAVE)
        try:  # Attempt to save the current data in the backup file.
            self.__create_save_file(data_folder)
            __save_file: str = join(data_folder, self.__file_name)
            with open(__save_file, "r", encoding="utf-8") as file:
                content: list[dict[str, Any]] = loads(file.read())
            content.append({key: self.data_manager[key] for key in data_keys})
            FileWriter.write_content(__save_file, content)
            self.__console.success(SAVE_MESSAGE.format(__save_file))
        except SaveFileError:  # The file is in use or deleted.
            self.__console.error(SAVE_ERROR)

    def save_upload(self) -> None:
        """Save all the details of the Pin for a new upload."""
        self.__save_content(UPLOAD_FOLDER, UPLOAD_DATA)
