# -*- coding: utf-8 -*-
# app/utils/update_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from io import BytesIO
from os.path import isdir, join
from os import getcwd
from pathlib import Path
from shutil import rmtree
from subprocess import Popen
from sys import executable
from tqdm import tqdm
from zipfile import ZipFile

from requests import get, Response

from app.constants.update import UPDATE_URL, PATHS_TO_REMOVE
from app.constants.messages import UPDATE_ERROR
from app.utils.exceptions import UpdateError
from app.utils.func import exit
from app.utils.logger.logger_manager import Logger


class UpdateManager:
    """This class provides methods to manage updating the tool.
    
    Methods:
    --------
        __call__() -> None:
            Performs the update process.

    Private methods:
    ---------------
        __download_new_version() -> bytes:
            Download the new version of the tool as a binary.

        __remove_previous_version() -> None:
            Remove the previous version of the tool.

        __install_new_version(file_binary_content: bytes) -> None:
            Install the new version of the tool.

        __launch_new_version() -> None:
            Launch the new version of the tool.

        __stop_previous_version() -> None:
            Stop the previous version of the tool.
    """
    
    def __download_new_version(self) -> bytes:
        """Download the new version of the tool as a binary.

        Returns:
        --------
            bytes: The binary content of the new version.

        Raises:
        -------
            UpdateError: If the ZIP archive cannot be retrieved
                from the backend.
        """
        response: Response = get(UPDATE_URL, stream=True, verify=False)
        # The ZIP archive cannot be retrieved from the backend.
        if not response.ok or not 200 <= response.status_code < 300:
            raise UpdateError(UPDATE_ERROR)
        # Define the file size according to the "Content-Length"
        # value present in the request response.
        content_length: str | int = response.headers.get('content-length', 0)
        total_size: int = int(content_length)
        # Download ZIP archive by data packet.
        file_binary_content: bytes = bytes()
        with tqdm(total=total_size, unit='iB', unit_scale=True,
                  unit_divisor=1024) as progress_bar:
            # Gradually add downloaded content to the binary.
            for binary_data in response.iter_content(chunk_size=1024):
                file_binary_content += binary_data
                progress_bar.update(len(binary_data))
        return file_binary_content
    
    def __remove_previous_version(self) -> None:
        """Remove the previous version of the tool.
        
        Delete each file and folder specified in `PATHS_TO_REMOVE`.
        """
        for path in PATHS_TO_REMOVE:  # Delete each file and folder.
            rmtree(path, ignore_errors=True) if isdir(path) \
                else Path(path).unlink(missing_ok=True)
    
    def __install_new_version(self, file_binary_content: bytes) -> None:
        """Install the new version of the tool.
        
        Recover the ZIP archive and extracts it to the root of the tool.

        Parameters:
        -----------
            file_binary_content (bytes): The binary content
                of the new version.
        """
        # Recover the ZIP and extract to the root of the tool.
        zip_file: ZipFile = ZipFile(BytesIO(file_binary_content))
        zip_file.extractall(getcwd())
    
    def __launch_new_version(self) -> None:
        """Launch the new version of the tool.
        
        Executes the "main.py" file of the new version using the
        current Python interpreter.
        """
        # Launch the new version by executing the `main.py` file.
        Popen([executable, join(getcwd(), 'main.py')])

    def __stop_previous_version(self) -> None:
        """Stop the previous version of the tool.
        
        Exit the current Python process to stop the previous version.
        """
        exit()

    def __call__(self) -> None:
        """Performs the update process.
        
        It includes the download, installation and launch of
        the new version, and removes and stops the previous version.
        """
        try:
            file_binary_content: bytes = self.__download_new_version()
            self.__remove_previous_version()
            self.__install_new_version(file_binary_content)
            self.__launch_new_version()
            self.__stop_previous_version()
        except (UpdateError, Exception):
            Logger.error()
