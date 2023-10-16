# -*- coding: utf-8 -*-
# app/services/tags/tags_process.py

"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""



from typing import Any, Dict, Generator, List
from app.services.login.cookie_manager import CookieManager
from app.services.login.user_manager import UserManager
from app.services.tags.tags_manager import TagsManager


class TagProcess(TagsManager, UserManager):
    """TagProcess is a class that handles the process of retrieving
    tags based on a query string using user cookies.

    Methods:
    --------
        __init__(self, query: str) -> None:
            Initialize a TagProcess instance with a query string.

    Private methods:
    ----------------
        __get_users_cookies(self) -> Generator[str, List[Any], None]:
            Retrieve valid user UUIDs from user data and yield them for
            use in tag retrieval.

        __retrieve_tags(self, uuid: str) -> List[Dict[str, Any]]:
            Retrieve tags using user cookies associated with the
            provided UUID.

        __call__(self) -> List[Dict[str, Any]]:
            Start the tag retrieval process and return the retrieved tags.

    Attributes:
    -----------
        __query (str): The query string used to search for tags.

    """
    
    def __init__(self, query: str) -> None:
        """Initialize a TagProcess instance with a query string.

        Parameters:
        -----------
            query (str): The query string used to search for tags.
        """
        self.__query: str = query
    
    def __get_users_cookies(self) -> Generator[str, List[Any], None]:
        """Retrieve valid user UUIDs from user data and yield them for
        use in tag retrieval.

        Yields:
        --------
            str: User UUIDs from the user data.
        """
        __users: List[UserManager.UserData] = self.retrieve_users_data()
        __valid_uuids: List[Any] = [user[1] for user in __users if user]
        yield from __valid_uuids + [None]  # Prevent StopIteration error.
        
    def __retrieve_tags(self, uuid: str) -> List[Dict[str, Any]]:
        """Retrieve tags using user cookies associated with the provided UUID.

        Parameters:
        -----------
            uuid (str): The UUID associated with user cookies.

        Returns:
        --------
            List[Dict[str, Any]]: A list of tags retrieved using the user
            cookies.
        """
        __cookies: Dict[str, Any] = CookieManager.retrieve_cookies_by_id(uuid)
        __tags_manager: TagsManager = TagsManager(__cookies)
        __tags: List[Dict[str, Any]] = __tags_manager(self.__query)
        return __tags
    
    def __call__(self) -> List[Dict[str, Any]]:
        """Start the tag retrieval process and return the retrieved tags.

        Returns:
        --------
            List[Dict[str, Any]]: A list of tags retrieved based on the
            query string and user cookies.
        """
        __uuids: Generator[str, List[str], None] = self.__get_users_cookies()
        __tags: List[Dict[str, Any]] = []
        while not __tags and (__uuid := next(__uuids)):
            __tags: List[Dict[str, Any]] = self.__retrieve_tags(__uuid)
        return __tags
