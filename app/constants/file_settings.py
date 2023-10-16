# -*- coding: utf-8 -*-
# app/constants/file_settings.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import Dict, List


FILE_PATH: str = 'file_path'
PINBOARD: str = 'pinboard'
TITLE: str = 'title'
DESCRIPTION: str = 'description'
ALT_TEXT: str = 'alt_text'
LINK: str = 'link'
TOPIC_TAGS: str = 'topic_tags'
DATETIME: str = 'datetime'
PAID_PIN: str = 'paid_pin'
COOKIES: str = 'cookies'
STARTING_VALUE: str = 'starting_value'
MAXIMUM_ATTEMPTS: str = 'maximum_attempts'
DELETE_TEMP_FILE: str = 'delete_temp_file'

# JSON keys used for each element.
UPLOAD_DATA: List[str] = [
    PAID_PIN,
    FILE_PATH,
    PINBOARD,
    TITLE,
    DESCRIPTION,
    ALT_TEXT,
    LINK,
    TOPIC_TAGS,
    DATETIME
]

TOPIC_TAGS_ID: str = 'id'
TOPIC_TAGS_VALUE: str = 'value'
TOPIC_TAGS_TAG_VALUE = 'tagValue'
TOPIC_TAGS_KEYS: List[str] = [
    TOPIC_TAGS_ID,
    TOPIC_TAGS_VALUE,
    TOPIC_TAGS_TAG_VALUE
]

# Constraints for certain keys used for elements.
DATA_LENGTH: Dict[str, int] = {
    TITLE: 100,
    DESCRIPTION: 500,
    ALT_TEXT: 500
}
LINK_DEFAULT_VALUE: str = 'https://'
ORGANIC_PIN: str = 'organic_pin'  # Paid pin already exists.

# Datetime format for `datetime.datetime` and `re`.
US_DATETIME_FORMAT: str = '%Y-%m-%d_%H-%M'  # File name.
DATETIME_FORMAT: str = '%d-%m-%Y %H:%M'
JS_DATETIME_FORMAT: str = '%d/%m/%Y %H:%M'
DATETIME_FORMAT_REGEX: str = r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}'
JS_DATETIME_FORMAT_REGEX: str = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'

IMAGE_TYPE: str = 'image'
VIDEO_TYPE: str = 'video'
IMAGE_PIN_TYPE: str = IMAGE_TYPE + '-story-pin'
VIDEO_PIN_TYPE: str = VIDEO_TYPE + '-story-pin'
PREVIEW_MAX_WIDTH: int = 256
