# -*- coding: utf-8 -*-
# app/services/login/cookie_manager.py

"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from copy import deepcopy
from genericpath import exists
from json import dumps, loads
from time import time
from typing import Any, Dict, List, Tuple
from uuid import uuid4

from app.constants.paths import COOKIES_FILE
from app.constants.webdriver import (
    ADDED_COOKIES_KEYS, LANGUAGE, PINTEREST_CSRF_COOKIE,
    PINTEREST_SESSION_COOKIE, TIMESTAMP, USERNAME, UUID)


class CookieManager:
    """Manages Pinterest cookies, their storage, and retrieval.

    This class provides methods for managing Pinterest cookies, including
    verifying their presence, retrieving them from a file, saving new cookies,
    editing existing cookies, and removing cookies from storage.

    Methods:
    --------
        verify_cookies(cookies: Dict[str, Any]) -> bool:
            Check if the required session cookies are present.
            
        same_uuid(cookies: Dict[str, Any],
                  cookies_: Dict[str, Any]) -> bool | None:
            Check if two sets of cookies have the same UUID or session cookie.

        retrieve_cookies_from_file() -> List[Dict[str, Any]]:
            Retrieve saved Pinterest cookies from a file.

        retrieve_cookies_by_id(id: str) -> Dict[str, Any]:
            Retrieve Pinterest cookies associated with a specific ID.

        add_cookies_to_file(cookies: Dict[str, Any]) -> None:
            Add new cookies to the storage.

        edit_cookies_from_file(cookies: Dict[str, Any]) -> None:
            Edit existing cookies in the storage.

        remove_cookies_from_file(cookies: Dict[str, Any]) -> None:
            Remove cookies from the storage.

        format_cookies(cookies: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
            Format Pinterest cookies for sending in requests.
            
    Private methods:
    ----------------
        __save_cookies(cookies: List[Dict[str, Any]]) -> None:
            Save Pinterest cookies to a file.
    """
            
    @staticmethod
    def verify_cookies(cookies: Dict[str, Any]) -> bool:
        """Check if the required session cookies are present.

        Returns:
        --------
            bool: True if the required cookies are present, otherwise False.
        """
        return PINTEREST_SESSION_COOKIE in cookies \
            and PINTEREST_CSRF_COOKIE in cookies
            
    @staticmethod
    def same_uuid(
            cookies: Dict[str, Any], cookies_: Dict[str, Any]) -> bool | None:
        """Check if two sets of cookies have the same UUID or session cookie.

        This static method compares two sets of cookies to check if they have
        the same UUID or session cookie, indicating whether they belong to
        the same user.

        Parameters:
        -----------
            cookies (Dict[str, Any]): The first set of cookies to compare.
            cookies_ (Dict[str, Any]): The second set of cookies to compare.

        Returns:
        --------
            bool | None: True if the cookies have the same UUID or session
            cookie, False if they are different, or None if the comparison
            cannot be made due to missing UUIDs or session cookies.
        """
        # Verify if both cookies have an UUID.
        __has_uuid: bool = UUID in cookies and UUID in cookies_
        # Verify if both cookies have the session cookie field.
        __valid_cookies: bool = CookieManager.verify_cookies(cookies)
        __valid_file_cookies: bool = CookieManager.verify_cookies(cookies_)
        if __has_uuid:  # We can compare both UUIDs.
            return cookies[UUID] == cookies_[UUID]
        # There is no UUIDs, we will compare session cookies.
        if __valid_cookies and __valid_file_cookies:
            # Create a shorter copy of the session cookie constant.
            __session_cookie: str = PINTEREST_SESSION_COOKIE
            return cookies[__session_cookie] == cookies_[__session_cookie]
        if not __valid_cookies and __valid_file_cookies:
            return False  # Keep the cookies in the file.

    @staticmethod
    def retrieve_cookies_from_file() -> List[Dict[str, Any]]:
        """Retrieve saved Pinterest cookies from a file.

        Returns:
        --------
            List[Dict[str, Any]]: A list of dictionaries containing
                saved cookies.
        """
        if not exists(COOKIES_FILE):  # The file containing the cookies
            return []  # does not exist, it will be created later.
        with open(COOKIES_FILE, 'r', encoding='utf-8') as file:
            return loads(file.read())
        
    @staticmethod
    def retrieve_cookies_by_id(id: str) -> Dict[str, Any]:
        """Retrieve Pinterest cookies associated with a specific ID.

        Parameters:
        -----------
            id (str): The ID associated with the cookies.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing the corresponding cookies.
        """
        __saved_cookies: List[Dict[str, Any]] = CookieManager\
            .retrieve_cookies_from_file()  # Retrieve saved cookies.
        for cookies in __saved_cookies:
            if USERNAME in cookies and cookies[UUID] == id:
                return cookies  # Return the corresponding cookies.
        return {}  # The corresponding cookies were not found.
    
    @staticmethod
    def __save_cookies(cookies: List[Dict[str, Any]]) -> None:
        """Save Pinterest cookies to a file.

        This method saves a list of Pinterest cookies to a file in
        JSON format.

        Parameters:
        -----------
            cookies (List[Dict[str, Any]]): A list of dictionaries containing
                Pinterest cookies to be saved.
        """
        with open(COOKIES_FILE, 'w+', encoding='utf-8') as file:
            file.write(dumps(cookies, indent=4))
            
    @staticmethod
    def add_cookies_to_file(cookies: Dict[str, Any]) -> None:
        """Add new cookies to the storage.

        Parameters:
        -----------
            cookies (Dict[str, Any]): A dictionary containing new cookies.
        """
        cookies.update({UUID: str(uuid4()), TIMESTAMP: time()})
        __saved_cookies: List[Dict[str, Any]] = \
            CookieManager.retrieve_cookies_from_file()
        __saved_cookies.append(cookies)
        CookieManager.__save_cookies(__saved_cookies)
        
    @staticmethod
    def edit_cookies_from_file(cookies: Dict[str, Any]) -> None:
        """Edit existing cookies in the storage.

        Parameters:
        -----------
            cookies (Dict[str, Any]): A dictionary containing
                updated cookies.
        """
        cookies.update({TIMESTAMP: time()})  # Renew timestamp.
        __saved_cookies: List[Dict[str, Any]] = CookieManager\
            .retrieve_cookies_from_file()  # Retrieve saved cookies.
        for index, current_cookies in enumerate(__saved_cookies[:]):
            if CookieManager.same_uuid(cookies, current_cookies):
                __saved_cookies[index] = cookies
        CookieManager.__save_cookies(__saved_cookies)
    
    @staticmethod
    def remove_cookies_from_file(cookies: Dict[str, Any]) -> None:
        """Remove cookies from the storage.

        Parameters:
        -----------
            cookies (Dict[str, Any]): A dictionary containing
                cookies to remove.
        """
        __saved_cookies: List[Dict[str, Any]] = CookieManager\
            .retrieve_cookies_from_file()  # Retrieve saved cookies.
        for index, current_cookies in enumerate(__saved_cookies[:]):
            __are_same_cookies: bool | None = CookieManager.same_uuid(
                cookies, current_cookies)  # True/None or False.
            # True: identical, False: different, None: error (remove).
            if __are_same_cookies in (True, None):
                __saved_cookies.pop(index)
        CookieManager.__save_cookies(__saved_cookies)
        
    @staticmethod
    def format_cookies(
            cookies: Dict[str, Any]) -> Tuple[str, Dict[str, Any], str]:
        """Format Pinterest cookies for sending in requests.

        Parameters:
        -----------
            cookies (Dict[str, Any]): A dictionary containing cookies.

        Returns:
        --------
            Tuple[str, Dict[str, Any], str]: A tuple containing the CSRF token
            and a dictionary of formatted cookies.
        """
        __cookies: Dict[str, Any] = deepcopy(cookies)
        __extension_domain: str = __cookies[LANGUAGE]
        __csrf_cookie: str = __cookies[PINTEREST_CSRF_COOKIE] \
            if PINTEREST_CSRF_COOKIE in cookies else ''
        [__cookies.pop(key) for key in ADDED_COOKIES_KEYS if key in __cookies]
        return __csrf_cookie, __cookies, __extension_domain
