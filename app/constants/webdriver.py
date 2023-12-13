# -*- coding: utf-8 -*-
# app/constants/webdriver.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import Final, List


DOMAIN_EXTENSION_REGEX: Final[str] = (
    r'^(https:\/\/[a-z]+\.[a-z]+(?:\.[a-z]+)?)\/?')

# Pinterest request URLs.
PINTEREST_URL: Final[str] = 'https://pinterest.com/'

PINTEREST_PIN_URL: Final[str] = PINTEREST_URL + 'pin/'
PINTEREST_SCHEDULE_PIN_URL: Final[str] = PINTEREST_URL + 'scheduled-pin/'
PINTEREST_LOGIN_URL: Final[str] = PINTEREST_URL + 'login/'

PINTEREST_RESOURCE_URL: Final[str] = '{}resource/'
PINTEREST_USER_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'UserSessionResource/create/')
PINTEREST_TAGS_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'ApiResource/get/')


# Pinterest upload request URLs.
PINTEREST_IMAGE_UPLOAD_URL: Final[str] = 'https://u.pinimg.com/'
PINTEREST_MEDIA_UPLOAD_URL: Final[str] = \
    'https://pinterest-media-upload.s3-accelerate.amazonaws.com/'

PINTEREST_AMAZON_ORGANIC_URL: Final[str] = '{}resource/ApiResource/create/'
PINTEREST_AMAZON_PAID_URL: Final[str] = '{}resource/VIPResource/create/'
PINTEREST_ETAG_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'VIPResource/get/')
PINTEREST_PINBOARD_ID_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'BoardPickerBoardsResource/get/')
PINTEREST_PIN_CONTENT_ORGANIC_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'StoryPinResource/create/')
PINTEREST_PIN_CONTENT_PAID_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'PinResource/create/')
PINTEREST_PIN_CONTENT_SCHEDULED_ORGANIC_URL: Final[str] = (
    PINTEREST_RESOURCE_URL + 'ScheduledPinResource/create/')
PINTEREST_PIN_CONTENT_SCHEDULED_PAID_URL: Final[str] = \
    PINTEREST_PIN_CONTENT_SCHEDULED_ORGANIC_URL


# Pinterest login and cookies verification.
PINTEREST_LOGIN_URL_MATCH: Final[str] = 'login'
PINTEREST_SESSION_COOKIE: Final[str] = '_pinterest_sess'
PINTEREST_CSRF_COOKIE: Final[str] = 'csrftoken'
PINTEREST_COOKIES_LIMIT: Final[int] = 30  # days.
JSON_FORMAT: Final[str] = 'application/json'

# Pinterest requests response's keys.
CONTENT_TYPE: Final[str] = 'content-type'
PINTEREST_CLIENT_CONTEXT: Final[str] = 'client_context'
PINTEREST_RESOURCE_RESPONSE: Final[str] = 'resource_response'
UPLOAD_PARAMETERS: Final[str] = 'upload_parameters'
UPLOAD_ID: Final[str] = 'upload_id'
STATUS: Final[str] = 'status'
SUCCESS: Final[str] = 'success'
ERROR: Final[str] = 'error'
MESSAGE: Final[str] = 'message'
MESSAGE_DETAIL: Final[str] = 'message_detail'
CODE: Final[str] = 'code'

# Pinterest cookies added keys.
LANGUAGE: Final[str] = 'language'  # Added but required for requests.
USERNAME: Final[str] = 'username'
IMAGE: Final[str] = 'profile_image'
TIMESTAMP: Final[str] = 'timestamp'
UUID: Final[str] = 'uuid'
ADDED_COOKIES_KEYS: Final[List[str]] = [
    USERNAME,
    IMAGE,
    TIMESTAMP,
    UUID,
    LANGUAGE
]

# Webdriver options.
CHROME_OPTIONS: Final[List[str]] = [
    '--log-level=3'
    '--mute-audio'
    '--disable-infobars'
    '--disable-popup-blocking'
    '--disable-dev-shm-usage'
    '--disable-gpu'
    '--no-sandbox'
]

# MacOS signature commands.
CODE_SIGN_UNSIGN: Final[str] = 'codesign --remove-signature "{}"'
CODE_SIGN_SIGN: Final[str] = 'codesign --force --deep -s - "{}"'
