from typing import Final

from app.constants.webdriver import (
    PINTEREST_PIN_URL,
    PINTEREST_URL,
)

# This file contains all the messages displayed on the tool
# interface or in the command prompt.

# Material icons.
ERROR_ICON: Final[str] = "error"
INFO_ICON: Final[str] = "info"
SUCCESS_ICON: Final[str] = "check_circle"


INTERNAL: Final[str] = "Internal"
PYTHON_VERSION_ERROR: Final[str] = (
    "Python 3.8 or earlier is required to use this tool.\nVersion used: {}"
)

REQUEST_ERROR: Final[str] = "An error occurred while processing the request."
PROCESS_HALTED: Final[str] = "[!] Process halted: {name} [{pid}]"

TOOL_NOT_ACTIVATED: Final[str] = "Please activate the tool."

# About the temporary folder and file.
TEMP_REMOVE_ERROR: Final[str] = "Cannot edit the temporary file."

# About the data file elements.
DATA_CHECKER_ERROR: Final[str] = "An error occurred while checking data."
DATA_FORMAT_ERROR: Final[str] = (
    "One or more of the required key data are missing."
)
FILE_PATH_VALUE_ERROR: Final[str] = "The asset file path is required."
FILE_PATH_ERROR: Final[str] = (
    "The file doesn't exist or its path is incorrect."
)
STRING_LENGTH_ERROR: Final[str] = (
    "The {key_name} should not exceed {max_length} characters."
)
PINBOARD_VALUE_ERROR: Final[str] = "The Pinboard is required for paid Pins."
EXTERNAL_LINK_ERROR: Final[str] = "The link format is incorrect."
TOPIC_TAGS_ERROR: Final[str] = "One of the topic tags is incorrect."
DATETIME_FORMAT_ERROR: Final[str] = "The datetime format is invalid."
DATETIME_PAST_ERROR: Final[str] = (
    "Cannot schedule a date that has already passed."
)
DATETIME_SCHEDULE_ERROR: Final[str] = "The schedule must be less than 14 days."
DATETIME_MINUTES_ERROR: Final[str] = "Time must be 0 or 30 minutes."

# About topic tags.
NO_TOPIC_TAGS_FOUND: Final[str] = (
    "No topic tags were found or no account is added to the tool."
)
TOPIC_TAGS_RETRIEVE_ERROR: Final[str] = (
    "An error occurred while retrieving the topic tags."
)

# About saving data files.
SAVE: Final[str] = "Save"
SAVE_MESSAGE: Final[str] = 'Data saved in the "{}" file.'
SAVE_ERROR: Final[str] = "Cannot save the data in the file."

# About the file and folder browsing.
BROWSE_FILE_CAPTION: Final[str] = "Select a JSON file."
BROWSE_FILE_FILTER: Final[str] = "JSON file (*.json)"
BROWSE_FOLDER_CAPTION: Final[str] = "Select a folder."

# About the webdriver.
WEBDRIVER: Final[str] = "Webdriver"
WEBDRIVER_DOWNLOAD: Final[str] = "Downloading the Webdriver."
WEBDRIVER_DOWNLOADED: Final[str] = "Webdriver downloaded."
WEBDRIVER_PATH_SET: Final[str] = "Webdriver found in the assets folder."
WEBDRIVER_DOWNLOAD_ERROR: Final[str] = "Webdriver download failed."
WEBDRIVER_PATCHING: Final[str] = "Patching the Webdriver."
WEBDRIVER_PATCHED: Final[str] = "Webdriver patched."
WEBDRIVER_NOT_PATCHED: Final[str] = "Webdriver not patched."
WEBDRIVER_SIGNING: Final[str] = "Modifying the ChromeDriver signature."
WEBDRIVER_SIGNED: Final[str] = "ChromeDriver signature modified."
WEBDRIVER_SIGNING_ERROR: Final[str] = (
    "ChromeDriver signature modification failed."
)
WEBDRIVER_RUN_ERROR: Final[str] = (
    "An error occurred while opening the webdriver."
)

# About the cookie retrieval.
LOGIN: Final[str] = "Login"
MANUAL_LOGIN: Final[str] = (
    "Please log in to your Pinterest account, the tool will retrieve "
    "the authentication cookies and stop the Webdriver automatically."
)
COOKIE_RETRIEVAL: Final[str] = "Retrieving cookies."
COOKIE_RETRIEVED: Final[str] = "Cookies retrieved and saved."
COOKIE_RETRIEVED_USER: Final[str] = (
    'Cookies retrieved and saved for "{}" user.'
)
COOKIE_RETRIEVAL_ERROR: Final[str] = "Cannot retrieve the cookies."

# About processes.
PROCESS_RUNNING: Final[str] = "Please stop any started process."
PROCESS_ERROR: Final[str] = (
    "An error occurred while starting or running the process."
)

# About the upload.
PIN: Final[str] = "Pin n&deg;{}/{}"  # &deg; = °
PIN_UPLOAD: Final[str] = "Uploading Pin."
PIN_SCHEDULE: Final[str] = "Scheduling Pin."
PIN_UPLOADED: Final[str] = "Pin uploaded."
PIN_SCHEDULED: Final[str] = "Pin scheduled."
PIN_UPLOAD_URL: Final[str] = (
    f'<a href="{PINTEREST_PIN_URL}{{id}}" target="_blank">'
    f"{PINTEREST_PIN_URL}{{id}}</a>"
)
PIN_SCHEDULE_URL: Final[str] = (
    f'<a href="{PINTEREST_URL}{{user}}/scheduled-pin/{{id}}" target="_blank">'
    f"{PINTEREST_URL}{{user}}/scheduled-pin/{{id}}</a>"
)
PIN_UPLOAD_ERROR: Final[str] = "Pin not uploaded."
AMAZON_CREDENTIALS_ERROR: Final[str] = (
    "An error occurred while retrieving Amazon upload credentials."
)
ETAG_ERROR: Final[str] = "An error occurred while retrieving ETag."
PINBOARDS_ERROR: Final[str] = (
    "An error occurred while retrieving Pinboards list."
)
PINBOARD_ID_ERROR: Final[str] = (
    "An error occurred while retrieving the Pinboard ID."
)
PIN_CONTENT_ERROR: Final[str] = "An error occurred while sending Pin content."
UPLOAD_FINISHED: Final[str] = "Process completed in {} hours and {} minutes."
RATE_LIMITED: Final[str] = "Upload limit reached. Waiting {} minute(s)."
