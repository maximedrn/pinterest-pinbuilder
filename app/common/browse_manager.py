# -*- coding: utf-8 -*-
# app/common/browse_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from os import DirEntry, getcwd, listdir, scandir
from os.path import isfile, join
from typing import List, Tuple

from app.constants.messages import (
    BROWSE_FILE_CAPTION, BROWSE_FILE_FILTER, BROWSE_FOLDER_CAPTION)
from app.constants.modules import PYQT5, PYQT6
from app.constants.paths import UPLOAD_FOLDER
from app.constants.version import OPERATING_SYSTEM_NAME, SYSTEM_VERSION


__install_pyqt5: bool = (
    # The current operating system matches the module.
    OPERATING_SYSTEM_NAME in PYQT5 and
    # The current operating system version matches the module.
    SYSTEM_VERSION in PYQT5[OPERATING_SYSTEM_NAME])
__install_pyqt6: bool = (
    # The current operating system matches the module.
    OPERATING_SYSTEM_NAME in PYQT6 and (
        # There are no operating system version prerequisites.
        not PYQT6[OPERATING_SYSTEM_NAME] or
        # The current operating system version matches the module.
        SYSTEM_VERSION in PYQT6[OPERATING_SYSTEM_NAME]))


if __install_pyqt6:
    from PyQt6.QtWidgets import QFileDialog, QApplication  # type: ignore
elif __install_pyqt5:
    from PyQt5.QtWidgets import QFileDialog, QApplication  # type: ignore


class BrowseManager:
    """BrowseManager class for handling file and folder browsing.

    Methods:
    --------
        __init__(self) -> None:
            Initialize the BrowseManager.
        
        browse_file(self) -> str:
            Open a file dialog and return the selected file's path.
        
        browse_folder(self) -> Tuple[str, int]:
            Open a folder dialog and return the selected folder's path
            and the number of files in it.
        
        retrieve_files_from_folder(
                folder_path: str, extension_name: str | None = None
                ) -> List[str]:
            Retrieve a list of files from a folder with optional
            filtering by file extension.
        
        retrieve_files_from_data_folder() -> List[str]:
            Retrieve a list of JSON files from a specific folder.

    Attributes:
    -----------
        __current_directory (str): The current working directory.
        __app (QApplication): The (unused) QApplication instance.
    """
    
    def __init__(self) -> None:
        """Initialize the BrowseManager.

        Initialize the current directory and creates a QApplication
        instance for GUI operations.
        """
        self.__current_directory: str = getcwd()
        self.__app: QApplication = QApplication([self.__current_directory])
    
    def browse_file(self) -> str:
        """Open a file dialog and return the selected file's path.

        Returns:
        --------
            str: The path of the selected file.
        """
        browsed_file: Tuple[str, str] = QFileDialog.getOpenFileName(
            parent=None, directory=self.__current_directory,
            caption=BROWSE_FILE_CAPTION, filter=BROWSE_FILE_FILTER,
            initialFilter=BROWSE_FILE_FILTER)
        return browsed_file[0]
    
    def browse_folder(self) -> Tuple[str, int]:
        """Open a folder dialog and return the selected folder's
        path and the number of files in it.

        Returns:
        --------
            Tuple[str, int]: A tuple containing the selected folder
                path and the number of files in it.
        """
        browsed_folder = QFileDialog.getExistingDirectory(
            parent=None, directory=self.__current_directory,
            caption=BROWSE_FOLDER_CAPTION)
        number_of_files: List[DirEntry[str]] | list = [
            file for file in scandir(browsed_folder) if isfile(file)] \
            if browsed_folder else []  # No folder were selected.
        return browsed_folder, len(number_of_files)
    
    @staticmethod
    def retrieve_files_from_folder(
            folder_path: str, extension_name: str | None = None) -> List[str]:
        """Retrieve a list of files from a folder with optional filtering
        by file extension.

        Parameters:
        -----------
            folder_path (str): The path to the folder.
            extension_name (str | None, optional): The file extension filter.
                Defaults to None.

        Returns:
        --------
            List[str]: A list of file paths that meet the filter criteria.
        """
        return [  # The path corresponds to a file and has correct extension.
            join(folder_path, path) for path in listdir(folder_path)
            if folder_path and isfile(join(folder_path, path)) and (
                # No extension for the files or a specific extension.
                not extension_name or path.endswith(extension_name))]
    
    @staticmethod
    def retrieve_files_from_data_folder() -> List[str]:
        """Retrieve a list of JSON files from a specific folder.

        Returns:
        --------
            List[str]: A list of paths to JSON files in the specified folder.
        """
        return BrowseManager.retrieve_files_from_folder(
            UPLOAD_FOLDER, '.json')
