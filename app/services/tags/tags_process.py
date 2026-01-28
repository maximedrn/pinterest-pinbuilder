from typing import Any, Generator

from app.constants.messages import NO_TOPIC_TAGS_FOUND
from app.constants.processes import CREATE_PROCESS
from app.services.login.cookie_manager import CookieManager
from app.services.login.user_manager import UserManager
from app.services.tags.tags_manager import TagsManager
from app.utils.logger.snackbar_manager import Snackbar


class TagProcess(TagsManager, UserManager):
    """TagProcess is a class that handles the process of retrieving
    tags based on a query string using user cookies.

    Methods:
    --------
        __init__(self, query: str) -> None:
            Initialize a TagProcess instance with a query string.

    Private methods:
    ----------------
        __get_users_cookies(self) -> Generator[str, list[Any], None]:
            Retrieve valid user UUIDs from user data and yield them for
            use in tag retrieval.

        __retrieve_tags(self, uuid: str) -> list[dict[str, Any]]:
            Retrieve tags using user cookies associated with the
            provided UUID.

        __call__(self) -> list[dict[str, Any]]:
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

    def __get_users_cookies(self) -> Generator[str, list[Any], None]:
        """Retrieve valid user UUIDs from user data and yield them for
        use in tag retrieval.

        Yields:
        --------
            str: User UUIDs from the user data.
        """
        __users: list[UserManager.UserData] = self.retrieve_users_data()
        __valid_uuids: list[Any] = [user[1] for user in __users if user]
        yield from __valid_uuids + [None]  # Prevent StopIteration error.

    def __retrieve_tags(self, uuid: str) -> list[dict[str, Any]]:
        """Retrieve tags using user cookies associated with the provided UUID.

        Parameters:
        -----------
            uuid (str): The UUID associated with user cookies.

        Returns:
        --------
            list[dict[str, Any]]: A list of tags retrieved using the user
            cookies.
        """
        __cookies: dict[str, Any] = CookieManager.retrieve_cookies_by_id(uuid)
        __tags_manager: TagsManager = TagsManager(__cookies)
        __tags: list[dict[str, Any]] = __tags_manager(self.__query)
        return __tags

    def __call__(self) -> list[dict[str, Any]]:
        """Start the tag retrieval process and return the retrieved tags.

        Returns:
        --------
            list[dict[str, Any]]: A list of tags retrieved based on the
            query string and user cookies.
        """
        __uuids: Generator[str, list[str], None] = self.__get_users_cookies()
        __tags: list[dict[str, Any]] = []
        while not __tags and (__uuid := next(__uuids)):
            __tags: list[dict[str, Any]] = self.__retrieve_tags(__uuid)
        if not __tags:  # Not tags or no account were added.
            Snackbar(CREATE_PROCESS).info(NO_TOPIC_TAGS_FOUND)
        return __tags
