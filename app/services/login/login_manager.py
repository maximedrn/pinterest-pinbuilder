from __future__ import annotations

from multiprocessing.managers import DictProxy
from re import Match, match
from time import sleep
from typing import Any

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.expected_conditions import url_contains
from selenium.webdriver.support.wait import WebDriverWait

from app.constants.messages import (
    COOKIE_RETRIEVAL,
    COOKIE_RETRIEVAL_ERROR,
    COOKIE_RETRIEVED,
    COOKIE_RETRIEVED_USER,
    LOGIN,
    MANUAL_LOGIN,
    WEBDRIVER_RUN_ERROR,
)
from app.constants.processes import LOGIN_PROCESS
from app.constants.webdriver import (
    DOMAIN_EXTENSION_REGEX,
    LANGUAGE,
    PINTEREST_LOGIN_URL,
    PINTEREST_LOGIN_URL_MATCH,
    PINTEREST_URL,
)
from app.services.login.cookie_manager import CookieManager
from app.services.login.user_manager import UserManager
from app.services.webdriver_manager import WebdriverManager
from app.utils.exceptions import CookieRetrievalError, WebdriverDownloadError
from app.utils.logger.console_manager import Console


class LoginManager(WebdriverManager):
    """Manage authentication on Pinterest and save session cookies.

    Methods:
    --------
        __init__(self) -> None:
            Initialize the LoginManager with default values.

        __call__(self) -> None:
            Perform the complete cookie retrieving on Pinterest.

    Private methods:
    ----------------
        __retrieve_domain_extension(self) -> str:
            Retrieve the domain extension (e.g., '.com', '.org') from
            the current URL.

        __retrieve_session_cookies(self) -> None:
            Retrieve session cookies from the WebDriver browser.

        __is_user_logged(self) -> None:
            Check if the user is logged to Pinterest.

    Attributes:
    -----------
        __session_cookies (dict): A dictionary to store session cookies.
        __logging_timeout (int): Maximum timeout for logging in, in seconds.
        __logging_timeout_frequency (int): Frequency for checking the login
            status in seconds.
        __retrieve_cookies_timeout (int): Timeout for retrieving cookies in
            seconds.
        __attempts (int): The current attempts when login.
        __attempts_limit (int): The maximum attempts that are accepted.
        __console (Console): The `Console` instance for logs.

    """

    def __init__(self) -> None:
        """Initialize the LoginManager with default values."""
        self.__session_cookies: dict[str, str] = {}
        self.__logging_timeout: int = 10 * 60  # second(s).
        self.__logging_timeout_frequency: int = 1  # second(s).
        self.__retrieve_cookies_timeout: int = 2  # second(s).
        self.__attempts: int = 0  # Current attempts.
        self.__attempts_limit: int = 5  # Maximum attempts.
        self.__console: Console = Console(LOGIN_PROCESS, LOGIN)
        super().__init__()

    def __retrieve_domain_extension(self) -> str:
        """Retrieve the domain extension (e.g., '.com', '.org') from
        the current URL.

        This method searches for a domain extension in the current URL using
        a regular expression pattern and returns the matched domain extension,
        or a default extension if not found.

        Returns:
        --------
            str: The domain extension (e.g., '.com') from the current URL,
            or a default extension if not found.
        """
        __regex: Match[str] | None = match(
            DOMAIN_EXTENSION_REGEX, self.driver.current_url
        )
        return __regex.group(1) if __regex else PINTEREST_URL

    def __retrieve_session_cookies(self) -> None:
        """Retrieve session cookies from the WebDriver browser."""
        self.__session_cookies: dict[str, str] = {
            web_cookie["name"]: web_cookie["value"]
            for web_cookie in self.driver.get_cookies()
        }
        __domain_extension: str = self.__retrieve_domain_extension()
        self.__session_cookies.update({LANGUAGE: __domain_extension})

    def __is_user_logged(self) -> None:
        """Check if the user is logged to Pinterest.

        It waits until the current URL is not the login URL.
        """
        WebDriverWait(
            driver=self.driver,
            timeout=self.__logging_timeout,
            poll_frequency=self.__logging_timeout_frequency,
        ).until_not(url_contains(PINTEREST_LOGIN_URL_MATCH))

    def __call__(self, manager: DictProxy[Any, Any]) -> None:
        """Perform the complete cookie retrieving on Pinterest.

        It includes opening the browser, navigating to the login page,
        verifying login, and saving session cookies.
        """
        try:
            self.__console.clear()  # Clear the console file.
            self.open_webdriver(manager)  # Open a new Selenium webdriver.
            # Browse the Pinterest login URL to allow the user to log in.
            Console(LOGIN_PROCESS, LOGIN).info(MANUAL_LOGIN)
            self.driver.get(PINTEREST_LOGIN_URL)
            self.__is_user_logged()  # Wait until the user logs in.
            self.__console.message(COOKIE_RETRIEVAL)
            while (
                self.__attempts < self.__attempts_limit
                and not CookieManager.verify_cookies(self.__session_cookies)
            ):
                # Retrieve session cookies and wait as long as required
                # the cookies are not found in the requests.
                sleep(self.__retrieve_cookies_timeout)
                self.__retrieve_session_cookies()
                self.__attempts += 1  # Increase the attempt counter.
            if self.__attempts >= self.__attempts_limit:
                raise CookieRetrievalError(COOKIE_RETRIEVAL_ERROR)
            # Save retrieved cookies for authentication in a file.
            CookieManager.add_cookies_to_file(self.__session_cookies)
            user_data: UserManager.UserData = UserManager().retrieve_user_data(
                self.__session_cookies
            )
            __message: str = (
                COOKIE_RETRIEVED_USER.format(user_data[0])
                if isinstance(user_data, tuple)
                else COOKIE_RETRIEVED
            )
            self.__console.success(__message)
        except (WebdriverDownloadError, WebDriverException):
            self.__console.error(WEBDRIVER_RUN_ERROR)
        except (CookieRetrievalError, Exception):
            self.__console.error(COOKIE_RETRIEVAL_ERROR)
