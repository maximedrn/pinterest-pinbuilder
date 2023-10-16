# -*- coding: utf-8 -*-
# app/utils/modules_manager.py

"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from os import system as os_system
from sys import executable
from typing import Dict, List, Tuple
from pkg_resources import working_set

from app.constants.modules import (
    MODULE_INSTALL_COMMAND, MODULE_INSTALL_FORMAT, MODULES_LIST)
from app.constants.version import OPERATING_SYSTEM_NAME, SYSTEM_VERSION


class ModulesManager:
    """This class provides methods to manage Python modules.
    
    It includes the compatibility checking, installation, and retrieval
    of modules to install.

    Attributes:
    -----------
        __required_modules (Dict[str, str]): A dictionary of required Python
            modules and their versions.

    Methods:
    --------
        install_modules() -> None:
            Install the required modules that are not already installed.

    Private methods:
    ----------------
        __module_os_compatibility(
                self, requirements: Dict[str, Tuple[str, str] | None] |
                Dict[str, Tuple[str, ...]] | None) -> bool:
            Check if a module is compatible with the current operating system.

        __module_installed(module: str, version: str | None) -> bool:
            Check if a module is installed with the correct version.

        __retrieve_modules_to_install() -> List[str]:
            Retrieve a list of modules to install based on compatibility.
    """
    
    def __init__(self) -> None:
        """Initialize the ModulesManager instance.
        
        It gathers information about required modules.
        """
        self.__required_modules: Dict[str, str] = {
            pkg.key: pkg.version for pkg in working_set}
    
    def __module_os_compatibility(
            self, requirements: Dict[str, Tuple[str, str] | Tuple] |
            Dict[str, Tuple[str, ...]] | None) -> bool:
        """Check if a module is compatible with the current operating system.

        Parameters:
        -----------
            requirements (
                    Dict[str, Tuple[str, str] | Tuple] |
                    Dict[str, Tuple[str, ...]] | None)):
                Operating system compatibility requirements.

        Returns:
        --------
            bool: True if the module is compatible; otherwise, False.
        """
        if not requirements:  # The requirements have not been specified.
            return True  # The module is not restricted on any system.
        if OPERATING_SYSTEM_NAME not in requirements:
            return False  # The module is not compatible with the system.
        if SYSTEM_VERSION not in requirements[OPERATING_SYSTEM_NAME]:
            return False  # The module is not compatible with the version.
        return True  # The system is compatible with the system.
    
    def __module_installed(self, module: str, version: str | None) -> bool:
        """Check if a module is installed with the correct version.

        Parameters:
        -----------
            module (str): The name of the module to check.
            version (str | None): The expected module version.

        Returns:
        --------
            bool: True if the module is installed and matches
                the version; otherwise, False.
        """
        if module not in self.__required_modules:
            return False  # The module is not installed.
        if version and self.__required_modules[module] != version:
            return False  # The module version does not match.
        return True  # The module is installed and its version is correct.
    
    def __retrieve_modules_to_install(self) -> List[str]:
        """Retrieve a list of modules to install based on compatibility.

        Returns:
        --------
            List[str]: A list of module names to install.
        """
        return [  # List of all required modules and their versions.
            MODULE_INSTALL_FORMAT.format(module=module, version=version)
            if version else module  # Just retrieves the module name.
            for module, (requirements, version) in MODULES_LIST.items()
            if self.__module_os_compatibility(requirements)
            and not self.__module_installed(module, version)]
            
    def install_modules(self) -> None:
        """Install the required modules that are not already installed.

        This method uses the `os.system()` method to run the Python command
        used to install modules.
        """
        __modules: List[str] = self.__retrieve_modules_to_install()
        if __modules:  # Modules need to be installed.
            os_system(MODULE_INSTALL_COMMAND.format(
                python=executable, modules=' '.join(__modules)))
