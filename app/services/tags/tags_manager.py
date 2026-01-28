from __future__ import annotations

from copy import deepcopy
from locale import getlocale
from typing import Any

from app.constants.file_settings import (
    TOPIC_TAGS_ID,
    TOPIC_TAGS_TAG_VALUE,
    TOPIC_TAGS_VALUE,
)
from app.constants.messages import TOPIC_TAGS_RETRIEVE_ERROR
from app.constants.processes import UPLOAD_PROCESS
from app.constants.request_body import (
    DATA,
    LANGUAGE,
    OPTIONS,
    QUERY,
    TAGS_BODY,
)
from app.constants.webdriver import PINTEREST_TAGS_URL
from app.services.login.cookie_manager import CookieManager
from app.services.request_manager import RequestManager
from app.utils.exceptions import RequestError
from app.utils.logger.snackbar_manager import Snackbar


class TagsManager(RequestManager):
    """TagsManager is a class responsible for handling the retrieval of tags
    based on a query using user cookies. It extends the RequestManager class
    for making HTTP requests.

    Methods:
    --------
        __init__(self, cookies: dict[str, Any]) -> None:
            Initialize a TagsManager instance with user cookies for making
            requests.

    Private methods:
    ----------------
        __get_user_language(self) -> str | None:
            Retrieve the user's language preference from the system.

        __get_request_body(self, query: str) -> dict[str, Any]:
            Generate a request body for retrieving tags based on the provided
            query.

        __extract_tags(
                self, response: dict[str, Any]) -> list[dict[str, Any]]:
            Extract and format tags from the response data.

        __call__(self, query: str) -> list[dict[str, Any]]:
            Start the process of retrieving tags based on the provided query.

    Attributes:
    -----------
        __language (str | None): The user's language preference, if available.
    """

    def __init__(self, cookies: dict[str, Any]) -> None:
        """Initialize a TagsManager instance with user cookies
        for making requests.

        Parameters:
        -----------
            cookies (dict[str, Any]): User cookies in dictionary format.

        """
        super().__init__(*CookieManager.format_cookies(cookies))

    def __get_user_language(self) -> str | None:
        """Retrieve the user's language preference from the system.

        Returns:
        --------
            str | None: The user's language preference or None if not found.
        """
        __found_language: str | None = getlocale()[0]
        if __found_language:
            return __found_language.split("_")[0]

    def __get_request_body(self, query: str) -> dict[str, Any]:
        """Generate a request body for retrieving tags based on the
        provided query.

        Parameters:
        -----------
            query (str): The query string used to search for tags.

        Returns:
        --------
            dict[str, Any]: A request body for tag retrieval.
        """
        __body: dict[str, Any] = deepcopy(TAGS_BODY)
        __body[DATA][OPTIONS][DATA][QUERY] = query
        if self.__language:  # Otherwise use the default language.
            __body[DATA][OPTIONS][DATA][LANGUAGE] = self.__language
        return __body

    def __extract_tags(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract and format tags from the response data.

        Parameters:
        -----------
            response (dict[str, Any]): The response data from tag retrieval.

        Returns:
        --------
            list[dict[str, Any]]: A list of formatted tags with their IDs
            and values.
        """
        __results: list[dict[str, Any]] = response[DATA]["results"]
        return [
            {
                TOPIC_TAGS_ID: tag["id"],
                TOPIC_TAGS_VALUE: tag["taxonomy_text"],
                TOPIC_TAGS_TAG_VALUE: tag["text"],
            }
            for tag in __results
        ]

    def __call__(self, query: str) -> list[dict[str, Any]]:
        """Start the process of retrieving tags based on the provided query.

        Parameters:
        -----------
            query (str): The query string used to search for tags.

        Returns:
        --------
            list[dict[str, Any]]: A list of tags retrieved based on
            the query string.
        """
        try:
            self.__language: str | None = self.__get_user_language()
            __body: dict[str, Any] = self.__get_request_body(query)
            __response: dict[str, Any] = self.post(
                PINTEREST_TAGS_URL, parameters=__body
            )
            self.request_error(__response, "")
            return self.__extract_tags(__response)
        except (Exception, RequestError):
            Snackbar(UPLOAD_PROCESS).error(TOPIC_TAGS_RETRIEVE_ERROR)
            return []
