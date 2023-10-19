# -*- coding: utf-8 -*-
# app/utils/license_key_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from json import dumps, loads
from os.path import exists
from re import match
from typing import Any, Dict

from requests import HTTPError, RequestException, Response, post

from app.constants.license_key import (
    LICENSE_KEY, LICENSE_KEY_COUNTER, LICENSE_KEY_REGEX, LICENSE_KEY_VALIDITY)
from app.constants.paths import LICENSE_KEY_FILE
from app.constants.webdriver import SUCCESS


class LicenseKeyManager:
    """This class provides methods to manage license keys
    
    It includes license key saving, retrieving, checking their
    validity and increasing the license key counter.

    Methods:
    --------
        save_license_key(license_key: str) -> None:
            Save the given license key to the license key file.

        retrieve_license_key() -> str:
            Retrieve the saved license key from the license key file.

        check_license_key_validity(license_key: str) -> bool:
            Check the validity of the given license key using the API.

        check_license_key_counter(license_key: str) -> bool:
            Check the license key using the API and increase the counter.

    Private methods:
    ----------------
        __load_api_response(response_text: str) -> Dict[str, Any]:
            Parse the API response text and return it as a dictionary.

        __check_license_key(license_key: str, api_url: str) -> bool:
            Check the license key against the specified API URL.
    """

    @staticmethod
    def save_license_key(license_key: str) -> None:
        """Save the given license key to the license key file.

        Parameters:
        -----------
            license_key (str): The license key to save.
        """
        with open(LICENSE_KEY_FILE, 'w+', encoding='utf-8') as file:
            file.write(dumps({LICENSE_KEY: license_key}, indent=4))

    @staticmethod
    def retrieve_license_key() -> str:
        """Retrieve the saved license key from the license key file.

        Returns:
        --------
            str: The retrieved license key.
        """
        if not exists(LICENSE_KEY_FILE):  # The file containing the license
            return ''  # key does not exist, it will be created later.
        with open(LICENSE_KEY_FILE, 'r', encoding='utf-8') as file:
            return loads(file.read())[LICENSE_KEY]
        
    @staticmethod
    def __load_api_response(response_text: str) -> Dict[str, Any]:
        """Parse the API response text and return it as a dictionary.

        Parameters:
        -----------
            response_text (str): The API response text.

        Returns:
        --------
            Dict[str, Any]: The parsed API response as a dictionary.
        """
        try:  # Try to convert the response string to a JSON object.
            return loads(response_text)  # Return the object if successful.
        except ValueError:  # The text is not in JSON format.
            # Return a false answer to invalidate the license key.
            return {SUCCESS: False}
        
    @staticmethod
    def __check_license_key(license_key: str, api_url: str) -> bool:
        """Check the license key against the specified API URL.

        Parameters:
        -----------
            license_key (str): The license key to check.
            api_url (str): The API URL to use for checking.

        Returns:
        --------
            bool: True if the license key is valid according to 
                the API; otherwise, False.
        """
        if not license_key or match(LICENSE_KEY_REGEX, license_key) is None:
            return False  # The license key is empty or in the wrong format.
        try:  # Try to check the license key by contacting the Gumroad API.
            url: str = api_url.format(license_key)
            response: Response = post(url, timeout=60, verify=False)
            result: Dict[str, Any] = LicenseKeyManager.\
                __load_api_response(response.text)
            return result[SUCCESS]  # Return the license key validity.
        except (HTTPError, RequestException):  # Network or API error.
            return LicenseKeyManager.__check_license_key(license_key, api_url)
        except Exception:  # Unexpected error when executing the try block.
            return False  # The key is considered invalid.
        
    @staticmethod
    def check_license_key_validity(license_key: str) -> bool:
        """Check the validity of the given license key using the API.

        Parameters:
        -----------
            license_key (str): The license key to check.

        Returns:
        --------
            bool: True if the license key is valid; otherwise, False.
        """
        return LicenseKeyManager.__check_license_key(
            license_key, LICENSE_KEY_VALIDITY)
        
    @staticmethod
    def check_license_key_counter(license_key: str) -> bool:
        """Check the license key using the API and increase the counter.

        Parameters:
        -----------
            license_key (str): The license key to check.

        Returns:
        --------
            bool: True if the license key is valid; otherwise, False.
        """
        return LicenseKeyManager.__check_license_key(
            license_key, LICENSE_KEY_COUNTER)
