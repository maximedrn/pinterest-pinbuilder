class RequiredValueError(Exception):
    """Raised when a required value is missing or not provided.

    This exception is used to signal that a certain value is required
    but has not been provided, resulting in an error condition.

    Example:
    --------
        raise RequiredValueError('The "username" field is required.')
    """


class IncorrectValueError(Exception):
    """Raised when a provided value is incorrect or invalid.

    This exception is used to indicate that a provided value is not
    within the expected or valid range, resulting in an error condition.

    Example:
    --------
        raise IncorrectValueError(
            'The title length must no exceed 100 characters.')
    """


class SaveFileError(Exception):
    """Raised when an error occurs while saving a file.

    This exception is used to handle errors related to file saving operations.

    Example:
    --------
        raise SaveFileError('Error occurred while saving the data to a file.')
    """


class DataFormatError(Exception):
    """Raised when data is in an incorrect or unexpected format.

    This exception is used when the format of data does not match
    the expected format.

    Example:
    --------
        raise DataFormatError('The data received is in an unexpected format.')
    """


class TempFileError(Exception):
    """Raised when an error occurs while working with temporary files.

    This exception is used to handle errors related to temporary
    file operations.

    Example:
    --------
        raise TempFileError(
            'Error occurred while working with temporary files.')
    """


class KillProcessError(Exception):
    """Raised when an error occurs while attempting to kill a process.

    This exception is used to handle errors related to process termination.

    Example:
    --------
        raise KillProcessError(
            'Error occurred while trying to terminate a process.')
    """


class KillListenerProcessError(Exception):
    """Raised when an error occurs while attempting to kill a listener task.

    This exception is used to handle errors related to terminating
    listener processes.

    Example:
    --------
        raise KillListenerProcessError(
            'Error occurred while terminating a listener process.')
    """


class WebdriverDownloadError(Exception):
    """Exception raised for errors during webdriver download.

    This exception is raised when an error occurs during the download
    of a webdriver for browser automation.

    Example:
    --------
        raise WebdriverDownloadError("Failed to download the Webdriver.")
    """


class WebdriverPatchError(Exception):
    """Exception raised for errors during webdriver patching.

    This exception is raised when an error occurs while patching a webdriver
    for browser automation.

    Example:
    --------
        raise WebdriverPatchError("Failed to patch the Webdriver.")
    """


class CookieRetrievalError(Exception):
    """Exception raised for errors during cookie retrieval.

    This exception is raised when there are issues retrieving cookies
    required for authentication.

    Example:
    --------
        raise CookieRetrievalError("Failed to retrieve cookies.")
    """


class RequestError(Exception):
    """Exception raised for errors during the upload process.

    This exception is raised when an error occurs during the upload process,
    such as failed uploads or other issues.

    Example:
    --------
        raise RequestError("Failed to upload the asset.")
    """


class LoggerError(Exception):
    """Exception raised for errors related to logging.

    This exception is raised when there are errors in the logging process,
    such as failures to write log entries or other logging-related issues.

    Example:
    --------
        raise LoggerError("Error occurred while sending log content.")
    """
