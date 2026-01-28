from __future__ import annotations

from app.constants.colors import GREEN, RED
from app.constants.messages import ERROR_ICON, INFO_ICON, SUCCESS_ICON
from app.utils.logger.logger_manager import Logger, LoggerManager


class Snackbar(LoggerManager):
    """A class for displaying snackbars with different types of messages,
    such as errors, info, and success messages. It extends the
    LoggerManager class for logging functionality.

    Methods:
    --------
        __init__(self, file_name: str) -> None:
            Initialize the Snackbar instance.

        error(self, message: str) -> None:
            Display an error snackbar with a custom message and log the
            associated error.

        info(self, message: str) -> None:
            Display an informational snackbar with a custom message.

        success(self, message: str) -> None:
            Display a success snackbar with a custom message.

    Private methods:
    ----------------
        __snackbar(self, message: str, icon: str,
                   color: str | None = None) -> None:
            Display a snackbar with a custom message, icon, and color.
    """

    def __snackbar(
        self, message: str, icon: str, color: str | None = None
    ) -> None:
        """Display a snackbar with a custom message, icon, and color.

        Parameters:
        -----------
            message (str): The message to display in the snackbar.
            icon (str): The icon to display in the snackbar.
            color (str | None, optional): The color of the snackbar.
                Defaults to None.
        """
        content: dict[str, str] = self._format_content(
            message=message, icon=icon, color=color
        )
        self._write_file([content])

    def error(self, message: str) -> None:
        """Display an error snackbar with a custom message and log
        the associated error.

        Parameters:
        -----------
            message (str): The error message to display in the snackbar.
        """
        Logger.error()
        self.__snackbar(message, ERROR_ICON, RED)

    def info(self, message: str) -> None:
        """Display an informational snackbar with a custom message.

        Parameters:
        -----------
            message (str): The information message to display in the snackbar.
        """
        self.__snackbar(message, INFO_ICON)

    def success(self, message: str) -> None:
        """Display a success snackbar with a custom message.

        Parameters:
        -----------
            message (str): The success message to display in the snackbar.
        """
        self.__snackbar(message, SUCCESS_ICON, GREEN)
