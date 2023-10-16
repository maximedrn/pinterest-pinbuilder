# -*- coding: utf-8 -*-
# app/interface.py

"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from multiprocessing import Manager
from multiprocessing.managers import DictProxy
from typing import Any, Callable, Dict, List, Tuple

from app.common.browse_manager import BrowseManager
from app.constants.messages import (
    LICENSE_KEY_NOT_VALID, LICENSE_KEY_PROCESS_RUNNING, PROCESS_ERROR,
    PROCESS_RUNNING, UPDATE_PROCESS_RUNNING)
from app.constants.processes import LOGIN_PROCESS, PROCESSES, UPLOAD_PROCESS
from app.constants.version import TOOL_VERSION
from app.services.create.create_manager import CreateManager
from app.services.login.user_manager import UserManager
from app.services.process_manager import ProcessManager
from app.services.tags.tags_process import TagProcess
from app.utils.license_key_manager import LicenseKeyManager
from app.utils.update_manager import UpdateManager
from app.utils.version_manager import VersionManager


class BaseManager:
    """BaseManager class for managing shared data and processes using a
    multiprocessing manager.

    This class provides a base manager for sharing data and managing processes
    in a multiprocessing manager. It includes methods for accessing and
    updating shared data, as well as checking whether specific processes are
    running.

    Methods:
    --------
        __init__(self) -> None:
            Initializes the BaseManager instance with an empty shared
            dictionary.

        __getitem__(self, key: str) -> Any:
            Retrieves a value from the shared dictionary using a key.

        __setitem__(self, key: str, value: Any):
            Sets a value in the shared dictionary using a key.

        is_process_running(self, process_name: str | None = None) -> bool:
            Checks if any process specified in the PROCESSES list is currently
            running. If a process_name is provided, it checks whether the
            specified process is running.

    Attributes:
    -----------
        __manager (DictProxy[Any, Any]): A shared dictionary for storing and
            managing data across multiple processes.
    """
    
    def __init__(self) -> None:
        """Initialize a BaseManager instance with an empty shared
        dictionary."""
        self.__manager: DictProxy[Any, Any] = Manager().dict()
    
    @property
    def manager(self) -> DictProxy[Any, Any]:
        """Property: Get the shared dictionary for data management.

        Returns:
        --------
            DictProxy[Any, Any]: A shared dictionary for storing and
            managing data.
        """
        return self.__manager
    
    def __getitem__(self, key: str) -> Any:
        """Get a value from the shared dictionary using a key.

        Parameters:
        -----------
            key (str): The key for the value to retrieve from the
                shared dictionary.

        Returns:
        --------
            Any: The value associated with the specified key in the
            shared dictionary.
        """
        return self.__manager.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value in the shared dictionary using a key.

        Parameters:
        -----------
            key (str): The key to associate with the value in the
                shared dictionary.
            value (Any): The value to store in the shared dictionary
                under the specified key.
        """
        self.__manager.update({key: value})
        
    def is_process_running(self, process_name: str | None = None) -> bool:
        """Check if specified processes are running.

        This method checks if any process specified in the PROCESSES list is
        currently running. If a process_name is provided, it checks whether
        the specified process is running.

        Parameters:
        -----------
            process_name (str | None): The name of the process to check. If
                provided, this method checks whether the specified process is
                running. If None, it checks if any process in the PROCESSES
                list is running.

        Returns:
        --------
            bool: True if the specified process is running (or any process in
            PROCESSES is running), False otherwise.
        """
        return any(self[process] for process in PROCESSES) \
            if not process_name else self[process_name]


class Interface(BaseManager):
    """Gateway for communication with methods called by the frontend.
    
    All methods are exposed using the `eel._expose()` method,
    which takes the method name and Callable as parameters.

    Methods:
        check_license_key(self) -> bool:
            Check if the license key is valid.

        retrieve_license_key(self) -> str:
            Retrieve the license key.

        retrieve_users_data(self) -> List[UserManager.UserData]:
            Retrieve user data.

        send_license_key(
                self, license_key: str) -> Tuple[bool | None, str | None]: 
            Send and validate the license key.

        retrieve_tool_changelog(self) -> List[str] | List:  
            Retrieve the tool's changelog.

        check_for_update(self) -> bool:
            Check if there is an update available.

        download_update(self, frontend_closed: bool = False) -> str | None:
            Download an update.

        browse_file(self) -> str:
        Open a file dialog for browsing a file.

        browse_folder(self) -> Tuple[str, int]:
            Open a folder dialog for browsing a folder.

        retrieve_files_from_data_folder(self) -> List[str]:
            Retrieve files from the data folder.

        start_creation_manager(
                self, assets_folder: str) -> Tuple[bool, str | None]:
            Start the creation manager.

        get_pin_data(self, index: int) -> Dict[str, Any] | dict:
            Get pin data by index.

        get_assets_preview_binary(self) -> List[str] | list:
            Get assets' preview binary data.

        load_next_chunk(self) -> bool:
            Load the next chunk of data.

        load_previous_chunk(self) -> bool:
            Load the previous chunk of data.

        apply_data_by_index(self, index: int, data: Dict[str, Any]) -> None:
            Apply data to a specific index.

        apply_for_all(self, key_name: str, value: str) -> None:
            Apply data to all items.

        delete_for_all(self, key_name: str) -> None:
            Delete data from all items.

        search_for_tags(self, query: str) -> List[Dict[str, Any]]:
            Search for tags based on a query.

        save_file(self) -> None:
            Save the file from the CreateManager.
    
    Attributes:
    -----------
        __browser_manager (BrowseManager): An instance of BrowseManager for
            browsing files and folders.
        __upload_manager (ProcessManager | None): An instance of
            ProcessManager for managing the
            upload process. Initialized as None.
        __login_manager (ProcessManager | None): An instance of ProcessManager
            for managing the login process. Initialized as None.
    """
    
    def __init__(self) -> None:
        """Initialize the Interface instance.

        Initializes the Interface instance and creates instances of
        BrowseManager for browsing files and folders. The upload and
        login managers are initialized as None.
        """
        self.__browser_manager: BrowseManager = BrowseManager()
        self.__upload_manager: ProcessManager | None = None
        self.__login_manager: ProcessManager | None = None
        super().__init__()
    
    def check_license_key(self) -> bool:
        """Check if the license key is valid.

        Returns:
        --------
            bool: True if the license key is valid, False otherwise.
        """
        license_key: str = self.retrieve_license_key()
        return LicenseKeyManager.check_license_key_validity(license_key)
    
    def retrieve_license_key(self) -> str:
        """Retrieve the license key.

        Returns:
        --------
            str: The license key.
        """
        return LicenseKeyManager.retrieve_license_key()
            
    def retrieve_users_data(self) -> List[UserManager.UserData]:
        """Retrieve user data.

        Returns:
        --------
            List[UserManager.UserData]: A list of user data.
        """
        return UserManager().retrieve_users_data()

    def send_license_key(
            self, license_key: str) -> Tuple[bool | None, str | None]:
        """Send and validate the license key.

        Parameters:
        -----------
            license_key (str): The license key to be validated.

        Returns:
        --------
            Tuple[bool | None, str | None]: A tuple containing a boolean 
            indicating success or None and a string message indicating
            the result or None.
        """
        if self.is_process_running():  
            return None, LICENSE_KEY_PROCESS_RUNNING
        LicenseKeyManager.save_license_key(license_key)
        if not self.check_license_key():
            return False, LICENSE_KEY_NOT_VALID
        return True, None
    
    def retrieve_tool_changelog(self) -> List[str] | List:
        """Retrieve the tool's changelog.

        Returns:
        --------
            List[str] | List: A list of strings representing the
            tool's changelog.
        """
        return VersionManager.retrieve_tool_changelog()
    
    def check_for_update(self) -> bool:
        """Check if there is an update available.

        Returns:
        --------
            bool: True if an update is available, False otherwise.
        """
        return TOOL_VERSION != VersionManager.retrieve_tool_version() != None
    
    def download_update(self, frontend_closed: bool = False) -> str | None:
        """Download an update.

        Parameters:
        -----------
            frontend_closed (bool, optional): Whether the frontend is
                closed. Defaults to False.

        Returns:
        --------
            str | None: A string message indicating the result or None.
        """
        if self.is_process_running():
            return UPDATE_PROCESS_RUNNING
        return UpdateManager()() if frontend_closed else None
    
    def browse_file(self) -> str:
        """Open a file dialog for browsing a file.

        Returns:
        --------
            str: The selected file path.
        """
        return self.__browser_manager.browse_file()
    
    def browse_folder(self) -> Tuple[str, int]:
        """Open a folder dialog for browsing a folder.

        Returns:
        --------
            Tuple[str, int]: A tuple containing the selected folder path
                and the number of files in that folder.
        """
        return self.__browser_manager.browse_folder()
    
    def retrieve_files_from_data_folder(self) -> List[str]:
        """Retrieve files from the data folder.

        Returns:
        --------
            List[str]: A list of file paths from the data folder.
        """
        return BrowseManager.retrieve_files_from_data_folder()
    
    def start_creation_manager(
            self, assets_folder: str) -> Tuple[bool, str | None]:
        """Start the creation manager.

        Parameters:
        -----------
            assets_folder (str): The path to the assets folder.

        Returns:
        --------
            Tuple[bool, str | None]: A tuple containing a boolean
            indicating success or None and a string message indicating
            the result or None.
        """
        if not self.check_license_key():
            return False, LICENSE_KEY_NOT_VALID
        self.__create: CreateManager = CreateManager(assets_folder)
        return True, None
    
    def __is_creation_started(self) -> bool:
        """Check if the creation manager has been started.

        Returns:
        --------
            bool: True if the creation manager is started, False otherwise.
        """
        return isinstance(self.__create, CreateManager)
        
    def get_pin_data(self, index: int) -> Dict[str, Any] | dict:
        """Get pin data for a specific index.

        Parameters:
        -----------
            index (int): The index of the pin.

        Returns:
        --------
            Dict[str, Any] | dict: A dictionary containing pin data or an
            empty dictionary if the creation manager is not started.
        """
        return self.__create[index] if self.__is_creation_started() else {}
    
    def get_assets_preview_binary(self) -> List[str] | list:
        """Get assets preview binary data.

        Returns:
        --------
            List[str] | list: A list of assets preview binary data or an
            empty list if the creation manager is not started.
        """
        return self.__create.get_assets_preview_binary() if \
            self.__is_creation_started() else []
    
    def load_next_chunk(self) -> bool:
        """Load the next chunk of pins.

        Returns:
        --------
            bool: True if the next chunk is loaded, False otherwise.
        """
        return self.__create.load_next_chunk() \
            if self.__is_creation_started() else False
    
    def load_previous_chunk(self) -> bool:
        """Load the previous chunk of pins.

        Returns:
        --------
            bool: True if the previous chunk is loaded, False otherwise.
        """
        return self.__create.load_previous_chunk() \
            if self.__is_creation_started() else False
        
    def apply_data_by_index(self, index: int, data: Dict[str, Any]) -> None:
        """Apply data to a pin by index.

        Parameters:
        -----------
            index (int): The index of the pin.
            data (Dict[str, Any]): A dictionary containing data to apply
                to the pin.
        """
        if self.__is_creation_started():
            self.__create.apply_data_by_index(index, data)
    
    def apply_for_all(self, key_name: str, value: str) -> None:
        """Apply a value to all pins for a specific key.

        Parameters:
        -----------
            key_name (str): The key to apply the value to.
            value (str): The value to apply.
        """
        if self.__is_creation_started():
            self.__create.apply_for_all(key_name, value)
        
    def delete_for_all(self, key_name:str) -> None:
        """Delete a key for all pins.

        Parameters:
        -----------
            key_name (str): The key to delete.
        """
        self.apply_for_all(key_name, '')
    
    def search_for_tags(self, query: str) -> List[Dict[str, Any]]:
        """Search for tags based on a query.

        Parameters:
        -----------
            query (str): The query for searching tags.

        Returns:
        --------
            List[Dict[str, Any]]: A list of dictionaries containing
            tag information.
        """
        return TagProcess(query)()
        
    def save_file(self) -> None:
        """Save the file from the CreateManager."""
        if self.__is_creation_started():
            self.__create.save_file()
    
    def __start_process(
            self, kwargs: Dict[str, Any], process_name: str,
            process_manager: Callable[..., bool]) -> Tuple[bool, str | None]:
        """Start a background process.

        Parameters:
        -----------
            kwargs (Dict[str, Any]): Keyword arguments for the process.
            process_name (str): The name of the process.
            process_manager (Callable[..., bool]): The process manager
                function.

        Returns:
        --------
            Tuple[bool, str | None]: A tuple containing a boolean
            indicating success or None and a string message indicating
            the result or None.
        """
        if not self.check_license_key():  # The license key is not valid:
            return False, LICENSE_KEY_NOT_VALID  # return an error.
        if self.is_process_running(UPLOAD_PROCESS):  # A process is already
            return False, PROCESS_RUNNING  # running: return an error.
        state: bool = process_manager(**kwargs)
        self[process_name] = state  # Change the process state.
        return state, (PROCESS_ERROR if not state else None)
    
    def __stop_process(
            self, process_name: str,
            process_manager: ProcessManager | None) -> None:
        """Stop a background process.

        Parameters:
        -----------
            process_name (str): The name of the process.
            process_manager (ProcessManager | None): The process manager
                instance.
        """
        if process_manager and self.is_process_running(process_name):
            process_manager.stop_process(process_name)
            self[process_name] = False
    
    def start_upload_process(
            self, kwargs: Dict[str, Any]) -> Tuple[bool, str | None]:
        """Start the upload process.

        Parameters:
        -----------
            kwargs (Dict[str, Any]): Keyword arguments for the upload process.

        Returns:
        --------
            Tuple[bool, str | None]: A tuple containing a boolean
            indicating success or None and a string message indicating
            the result or None.
        """
        __upload_manager: ProcessManager = ProcessManager(self.manager)
        self.__upload_manager: ProcessManager | None = __upload_manager
        return self.__start_process(  # Send the function to call and the
            kwargs, UPLOAD_PROCESS,  # different arguments to start the
            self.__upload_manager.start_upload_process)  # upload.

    def start_login_process(self) -> Tuple[bool, str | None]:
        """Start the login process.

        Returns:
        --------
            Tuple[bool, str | None]: A tuple containing a boolean
            indicating success or None and a string message indicating
            the result or None.
        """
        __login_manager: ProcessManager = ProcessManager(self.manager)
        self.__login_manager: ProcessManager | None = __login_manager
        return self.__start_process(  # Send the function to call.
            {}, LOGIN_PROCESS, self.__login_manager.start_login_process)

    def stop_login_process(self) -> None:
        """Stop the login process."""
        self.__stop_process(LOGIN_PROCESS, self.__login_manager)

    def stop_upload_process(self) -> None:
        """Stop the upload process."""
        self.__stop_process(UPLOAD_PROCESS, self.__upload_manager)
