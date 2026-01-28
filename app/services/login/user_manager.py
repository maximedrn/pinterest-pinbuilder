from __future__ import annotations

from datetime import datetime as dt
from datetime import timedelta
from typing import Any
from uuid import uuid4

from app.constants.request_body import USER_DATA_BODY
from app.constants.webdriver import (
    ADDED_COOKIES_KEYS,
    ERROR,
    IMAGE,
    PINTEREST_COOKIES_LIMIT,
    PINTEREST_USER_URL,
    TIMESTAMP,
    USERNAME,
    UUID,
)
from app.services.login.cookie_manager import CookieManager
from app.services.request_manager import RequestManager


class UserManager(RequestManager):
    """UserManager class for managing user-related functionality.

    This class handles user data retrieval and management.

    Methods:
        __init__(self) -> None:
            Prevent overwriting from inheritance when instanced.

        verify_cookies_validity(self, cookies: dict[str, Any]) -> bool:
            Verify the validity of user cookies.

        verify_cookies_field(self, cookies: dict[str, Any]) -> bool:
            Verify if required cookies are present and within the time limit.

        retrieve_user_data(
                self, cookies: dict[str, Any]) -> UserManager.UserData:
            Retrieve user data based on provided cookies.

        retrieve_users_data(self) -> list[UserManager.UserData]:
            Retrieve user data for multiple users.

    Private methods:
    ----------------
        __get_cookies(self) -> list[dict[str, Any]]:
            Retrieve cookies from a file.

        __post_request(self, body: dict[str, str]) -> dict[str, Any]:
            Send a POST request to retrieve user data.

        __verify_user_data(
                self, response: dict[str, Any],
                cookies: dict[str, Any]) -> UserManager.UserData:
            Verify user data received in the response and update cookies.

        __extract_user_data(
                self, cookies: dict[str, Any]) -> UserManager.UserData:
            Extract user data from the provided cookies.
    """

    UserData = tuple[str, str, str, float] | None

    def __init__(self) -> None:
        """Prevent overwriting from inheritance when instanced."""

    def verify_cookies_validity(self, cookies: dict[str, Any]) -> bool:
        """Verify the validity of user cookies.

        This method checks if the provided user cookies are still valid by
        comparing the timestamp within the cookies to the current time and
        a predefined cookies expiration limit. If the cookies have expired,
        they are removed from storage.

        Parameters:
        -----------
            cookies (dict[str, Any]): User cookies in dictionary format.

        Returns:
        --------
            bool: True if the cookies are still valid, False if they have
            expired.
        """
        __cookies_timestamp: dt = dt.fromtimestamp(cookies[TIMESTAMP])
        __time_difference: timedelta = dt.now() - __cookies_timestamp
        __limit: timedelta = timedelta(days=PINTEREST_COOKIES_LIMIT)
        valid_cookies: bool = __time_difference < __limit
        if not valid_cookies:  # The cookies has expired.
            CookieManager.remove_cookies_from_file(cookies)
        return valid_cookies

    def verify_cookies_field(self, cookies: dict[str, Any]) -> bool:
        """Verify if required cookies are present and within the time limit.

        Parameters:
        -----------
            cookies (dict[str, Any]): A dictionary containing cookies.

        Returns:
        --------
            bool: True if the cookies are valid, False otherwise.
        """
        return not any(
            key not in cookies or not cookies[key]
            for key in ADDED_COOKIES_KEYS
        )  # Keys must be present.

    def __get_cookies(self) -> list[dict[str, Any]]:
        """Retrieve cookies from a file.

        Returns:
        --------
            list[dict[str, Any]]: A list of dictionaries containing cookies.
        """
        return CookieManager.retrieve_cookies_from_file()

    def __post_request(self) -> dict[str, Any]:
        """Send a POST request to retrieve user data.

        Returns:
        --------
            dict[str, Any]: The response from the POST request.
        """
        return self.post(
            PINTEREST_USER_URL,
            parameters=USER_DATA_BODY,
            resource_response=False,
        )

    def __verify_user_data(
        self, response: dict[str, Any], cookies: dict[str, Any]
    ) -> UserManager.UserData:
        """Verify user data received in the response and update cookies.

        This method extracts user-related information from a response and
        updates the cookies with the user's username, image profile URL,
        UUID, and timestamp. If UUID and timestamp are not present in the
        cookies, new values are generated and applied.

        Parameters:
        -----------
            response (dict[str, Any]): A dictionary containing user-related
                information in the response.
            cookies (dict[str, Any]): A dictionary containing cookies to be
                updated with user data.

        Returns:
        --------
            UserManager.UserData: An object representing user data.
        """
        username: str = response["user"]["username"]
        image_profile: str = response["user"]["image_large_url"]
        # Check if the UUID and timestamp are still existing (they should!).
        __has_uuid: bool = UUID in cookies and cookies[UUID]
        __has_timestamp: bool = TIMESTAMP in cookies and cookies[TIMESTAMP]
        # Retrieve the values or create new values and then apply them.
        uuid: str = cookies[UUID] if __has_uuid else str(uuid4())
        timestamp: float = (
            cookies[TIMESTAMP] if __has_timestamp else dt.now().timestamp()
        )  # Get the current timestamp.
        cookies.update({USERNAME: username, IMAGE: image_profile})
        cookies.update({UUID: uuid, TIMESTAMP: timestamp})
        CookieManager.edit_cookies_from_file(cookies)
        return username, uuid, image_profile, timestamp

    def __extract_user_data(
        self, cookies: dict[str, Any]
    ) -> UserManager.UserData:
        """Extract user data from the provided cookies.

        This method extracts user data, including username, UUID,
        image URL, and timestamp, from the given cookies.

        Parameters:
        -----------
            cookies (dict[str, Any]): User cookies in dictionary format.

        Returns:
        --------
            UserManager.UserData: A tuple containing user data (username,
            UUID, image URL, timestamp).
        """
        return (
            cookies[USERNAME],
            cookies[UUID],
            cookies[IMAGE],
            cookies[TIMESTAMP],
        )

    def retrieve_user_data(
        self, cookies: dict[str, Any]
    ) -> UserManager.UserData:
        """Retrieve user data based on provided cookies.

        Parameters:
        -----------
            cookies (dict[str, str]): A dictionary containing cookies.

        Returns:
        --------
            UserManager.UserData: A tuple containing user data
            (username, image URL, UUID, timestamp), or None
            if there was an error.
        """
        super().__init__(*CookieManager.format_cookies(cookies))
        __response: dict[str, Any] = self.__post_request()
        if ERROR not in __response:  # The username is retrieved.
            return self.__verify_user_data(__response, cookies)
        CookieManager.remove_cookies_from_file(cookies)

    def retrieve_users_data(self) -> list[UserManager.UserData]:
        """Retrieve user data for multiple users.

        Returns:
        --------
            list[UserManager.UserData]: A list of tuples containing
            user data (username, image URL, UUID) for multiple users.
        """
        __cookies: list[dict[str, Any]] = self.__get_cookies()
        usernames: list[UserManager.UserData] = []
        for cookies in __cookies:
            if not self.verify_cookies_validity(cookies):
                continue  # The cookies are not valid and removed.
            if not self.verify_cookies_field(cookies):
                usernames.append(self.retrieve_user_data(cookies))
                continue  # Cookies retrieved from the request.
            usernames.append(self.__extract_user_data(cookies))
        # Remove empty usernames from the list and return it.
        return [username for username in usernames if username]
