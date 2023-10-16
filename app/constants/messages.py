# -*- coding: utf-8 -*-
# app/constants/messages.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


# This file contains all the messages displayed on the tool
# interface or in the command prompt.

# Material icons.
from app.constants.webdriver import PINTEREST_PIN_URL


ERROR_ICON: str = 'error'
INFO_ICON: str = 'info'
SUCCESS_ICON: str = 'check_circle'


INTERNAL: str = 'Internal'
PYTHON_VERSION_ERROR: str = (
    'Python 3.8 or earlier is required to use this tool.\nVersion used: {}')

REQUEST_ERROR: str = 'An error occurred while processing the request.'
PROCESS_HALTED: str = '[!] Process halted: {name} [{pid}]'

# About the license key.
LICENSE_KEY_NOT_VALID: str = 'The license key is not valid.'
LICENSE_KEY_PROCESS_RUNNING: str = (
    'It is not possible to change the license key while a process '
    'is running.')
TOOL_NOT_ACTIVATED: str = 'Please activate the tool.'

# About the update.
UPDATE_ERROR: str = 'An error occurred while fetching the new update.'
UPDATE_PROCESS_RUNNING: str = (
    'Please stop any running process before updating the tool.')
    
# About the temporary folder and file.
TEMP_REMOVE_ERROR: str = 'Cannot edit the temporary file.'

# About the data file elements.
DATA_CHECKER_ERROR: str = 'An error occurred while checking data.'
DATA_FORMAT_ERROR: str = 'One or more of the required key data are missing.'
FILE_PATH_VALUE_ERROR: str = 'The "file_path" value is required.'
FILE_PATH_ERROR: str = 'The file doesn\'t exist or its path is incorrect.'
STRING_LENGTH_ERROR: str = (
    'The {key_name} should not exceed {max_length} characters.')
EXTERNAL_LINK_ERROR: str = 'The link format is incorrect.'
TOPIC_TAGS_ERROR: str = 'One of the topic tags is incorrect.'
DATETIME_FORMAT_ERROR: str = 'The datetime format is invalid.'
DATETIME_PAST_ERROR: str = 'Cannot schedule a date that has already passed.'
DATETIME_SCHEDULE_ERROR: str = 'The schedule must be less than 14 days.'
DATETIME_MINUTES_ERROR: str = 'Time must be 0 or 30 minutes.'

# About saving data files.
SAVE: str = 'Save'
SAVE_MESSAGE: str = 'Data saved in the {} file.'
SAVE_ERROR: str = 'Cannot save the data in the file.'

# About the file and folder browsing.
BROWSE_FILE_CAPTION: str = 'Select a JSON file.'
BROWSE_FILE_FILTER: str = 'JSON file (*.json)'
BROWSE_FOLDER_CAPTION: str = 'Select a folder.'

# About the webdriver.
WEBDRIVER: str = 'Webdriver'
WEBDRIVER_DOWNLOAD: str = 'Downloading the Webdriver.'
WEBDRIVER_DOWNLOADED: str = 'Webdriver downloaded.'
WEBDRIVER_PATH_SET: str = 'Webdriver found in the assets folder.'
WEBDRIVER_DOWNLOAD_ERROR: str = 'Webdriver download failed.'
WEBDRIVER_PATCHING: str = 'Patching the Webdriver.'
WEBDRIVER_PATCHED: str = 'Webdriver patched.'
WEBDRIVER_NOT_PATCHED: str = 'Webdriver not patched.'

# About the cookie retrieval.
LOGIN: str = 'Login'
MANUAL_LOGIN: str = (
    'Please log in to your Pinterest account, the tool will retrieve '
    'the authentication cookies and stop the Webdriver automatically.')
COOKIE_RETRIEVAL: str = 'Retrieving cookies.'
COOKIE_RETRIEVED: str = 'Cookies retrieved and saved.'
COOKIE_RETRIEVED_USER: str = 'Cookies retrieved and saved for "{}" user.'
COOKIE_RETRIEVAL_ERROR: str = 'Cannot retrieve the cookies.'

# About processes.
PROCESS_RUNNING: str = 'Please stop any started process.'
PROCESS_ERROR: str = 'An error occurred while starting or running the process.'

# About the upload.
PIN_UPLOAD: str = 'Pin n&deg;{}/{}'  # &deg; = °
PIN_UPLOAD_RUNNING: str = 'Uploading Pin.'
PIN_UPLOAD_SUCCESS: str = 'Pin uploaded.'
PIN_UPLOAD_URL: str = (
    f'<a href="{PINTEREST_PIN_URL}{{id}}" target="_blank">'
    f'{PINTEREST_PIN_URL}{{id}}</a>')
PIN_UPLOAD_ERROR: str = 'Pin not uploaded.'
AMAZON_CREDENTIALS_ERROR: str = (
    'An error occurred while retrieving Amazon upload credentials.')
ETAG_ERROR: str = 'An error occurred while retrieving ETag.'
PINBOARDS_ERROR: str = 'An error occurred while retrieving Pinboards list.'
PINBOARD_ID_ERROR: str = 'An error occurred while retrieving the Pinboard ID.'
PIN_CONTENT_ERROR: str = 'An error occurred while sending Pin content.'
UPLOAD_FINISHED: str = 'Process completed in {} hours and {} minutes.'
