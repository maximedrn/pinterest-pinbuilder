# -*- coding: utf-8 -*-
# app/constants/webdriver.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import List


DOMAIN_EXTENSION_REGEX: str = r'https?://(?:www\.)?pinterest\.([a-zA-Z]+)/'
DEFAULT_DOMAIN_EXTENSION: str = 'com'

# Pinterest request URLs.
PINTEREST_BASE_URL: str = 'https://pinterest.{}/'
PINTEREST_URL: str = PINTEREST_BASE_URL.format(DEFAULT_DOMAIN_EXTENSION)

PINTEREST_PIN_URL: str = PINTEREST_URL + 'pin/'
PINTEREST_LOGIN_URL: str = PINTEREST_URL + 'login/'
PINTEREST_RESOURCE_URL: str = PINTEREST_BASE_URL + 'resource/'
PINTEREST_USER_URL: str = (
    PINTEREST_RESOURCE_URL + 'UserSessionResource/create/')
PINTEREST_TAGS_URL: str = (
    PINTEREST_RESOURCE_URL + 'ApiResource/get/')

# Pinterest upload request URLs.
PINTEREST_IMAGE_UPLOAD_URL: str = 'https://u.pinimg.com/'
PINTEREST_MEDIA_UPLOAD_URL: str = \
    'https://pinterest-media-upload.s3-accelerate.amazonaws.com/'
PINTEREST_AMAZON_ORGANIC_URL: str = (
    PINTEREST_BASE_URL + 'resource/ApiResource/create/')
PINTEREST_AMAZON_PAID_URL: str = (
    PINTEREST_BASE_URL + 'resource/VIPResource/create/')
PINTEREST_ETAG_URL: str = (
    PINTEREST_RESOURCE_URL + 'VIPResource/get/')
PINTEREST_PINBOARD_ID_URL: str = (
    PINTEREST_RESOURCE_URL + 'BoardPickerBoardsResource/get/')
PINTEREST_PIN_CONTENT_ORGANIC_URL: str = (
    PINTEREST_RESOURCE_URL + 'StoryPinResource/create/')
PINTEREST_PIN_CONTENT_PAID_URL: str = (
    PINTEREST_RESOURCE_URL + 'PinResource/create/')

# Pinterest login and cookies verification.
PINTEREST_LOGIN_URL_MATCH: str = 'login'
PINTEREST_SESSION_COOKIE: str = '_pinterest_sess'
PINTEREST_CSRF_COOKIE: str = 'csrftoken'
PINTEREST_COOKIES_LIMIT: int = 30  # days.
JSON_FORMAT: str = 'application/json'

# Pinterest requests response's keys.
CONTENT_TYPE: str = 'content-type'
PINTEREST_CLIENT_CONTEXT: str = 'client_context'
PINTEREST_RESOURCE_RESPONSE: str = 'resource_response'
UPLOAD_PARAMETERS: str = 'upload_parameters'
UPLOAD_ID: str = 'upload_id'
STATUS: str = 'status'
SUCCESS: str = 'success'
ERROR: str = 'error'

# Pinterest cookies added keys.
LANGUAGE: str = 'language'  # Added but required for requests.
USERNAME: str = 'username'
IMAGE: str = 'profile_image'
TIMESTAMP: str = 'timestamp'
UUID: str = 'uuid'
ADDED_COOKIES_KEYS: List[str] = [
    USERNAME,
    IMAGE,
    TIMESTAMP,
    UUID,
    LANGUAGE
]

# Webdriver options.
CHROME_OPTIONS: List[str] = [
    '--log-level=3'
    '--mute-audio'
    '--disable-infobars'
    '--disable-popup-blocking'
    '--disable-dev-shm-usage'
    '--disable-gpu'
    '--no-sandbox'
]
