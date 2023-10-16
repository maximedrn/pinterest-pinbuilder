# -*- coding: utf-8 -*-
# app/constants/request_body.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import Any, Dict, List

from app.constants.file_settings import (
    ALT_TEXT, DESCRIPTION, LINK, TOPIC_TAGS)


# Default keys of the request bodies.
SOURCE_URL: str = 'source_url'
DATA: str = 'data'
OPTIONS: str = 'options'
URL: str = 'url'

# Current sub-paths used by Pinterest.
ORGANIC_PIN_URL: str = '/pin-creation-tool/'
PAID_PIN_URL: str = '/pin-builder/'
AMAZON_UPLOAD_URL: str = '/v3/media/uploads/register/batch/'
TAGS_URL: str = '/v3/manual_tags/search/'

# User data (name and profile picture) request.
SESSION_ACCOUNTS: str = 'session_accounts'

USER_DATA_BODY: Dict[str, Any] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {
            SESSION_ACCOUNTS: True
        }
    }
}


# Tags request.
LANGUAGE: str = 'language'
DEFAULT_LANGUAGE: str = 'en'
QUERY: str = 'query'
CORPUS: str = 'corpus'
CORPUS_VALUE: str = 'interests'
LIMIT: str = 'limit'
MIN_LEVEL: str = 'min_level'

TAGS_BODY: Dict[str, Any] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {
            URL: TAGS_URL,
            DATA: {
                LANGUAGE: DEFAULT_LANGUAGE,
                QUERY: None,
                CORPUS: CORPUS_VALUE,
                LIMIT: 10,
                MIN_LEVEL: 3
            }
        }
    }
}


# Amazon credentials request for organic Pin.
FILE: str = 'file'
ID: str = 'id'
MEDIA_INFO_LIST: str = 'media_info_list'
MEDIA_TYPE: str = 'media_type'

MEDIA_INFO_LIST_VALUE: List[Dict[str, Any]] = [
    {ID: None, MEDIA_TYPE: None},
    {ID: None, MEDIA_TYPE: None}
]


AMAZON_CREDENTIALS_BODY_ORGANIC: Dict[str, Any] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {
            URL: AMAZON_UPLOAD_URL,
            DATA: {MEDIA_INFO_LIST: {}}
        }
    }
}

# Amazon credentials request for paid Pin.
TYPE: str = 'type'
IMAGE_PAID_PIN: str = 'pinimage'
VIDEO_PAID_PIN: str = 'video'

AMAZON_CREDENTIALS_BODY_PAID: Dict[str, Any] = {
    SOURCE_URL: PAID_PIN_URL,
    DATA: {
        OPTIONS: {
            TYPE: None
        }
    }
}


# ETag request.
UPLOAD_IDS: str = 'upload_ids'

ETAG_BODY: Dict[str, Any] = {
    SOURCE_URL: None,
    DATA: {
        OPTIONS: {
            UPLOAD_IDS: []
        }
    }
}


# Pinboard ID request.
FIELD_SET_KEY: str = 'field_set_key'
FIELD_SET_KEY_VALUE: str = 'board_picker'
FILTER: str = 'filter'
FILTER_VALUE: str = 'all'

PINBOARD_ID_BODY: Dict[str, Any] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {
            FIELD_SET_KEY: FIELD_SET_KEY_VALUE,
            FILTER: FILTER_VALUE
        }
    }
}

# Pin content request.
BOARD_ID: str = 'board_id'
SCHEDULED_TIMESTAMP: str = 'scheduled_timestamp'
ALLOW_SHOPPING: str = 'allow_shopping_rec'
IS_COMMENTS_ALLOWED: str = 'is_comments_allowed'
IS_UNIFIED_BUILDER: str = 'is_unified_builder'
IS_REMOVABLE: str = 'is_removable'
STORY_PIN: str = 'story_pin'
METADATA: str = 'metadata'
PIN_TITLE: str = 'pin_title'
PIN_IMAGE_SIGNATURE: str = 'pin_image_signature'
IMAGE_SIGNATURE: str = 'image_signature'
VIDEO_SIGNATURE: str = 'video_signature'
PAGES: str = 'pages'
BLOCKS: str = 'blocks'
BLOCK_STYLE: str = 'block_style'
TYPE: str = 'type'
LAYOUT: str = 'layout'

BLOCK_STYLE_VALUE: Dict[str, int] = {
    'height': 100,
    'width': 100,
    'x_coord': 0,
    'y_coord': 0
}

PIN_CONTENT_ORGANIC_BODY: Dict[str, Any] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {
            DESCRIPTION: None,
            BOARD_ID: None,
            LINK: None,
            ALLOW_SHOPPING: True,
            IS_COMMENTS_ALLOWED: True,
            IS_UNIFIED_BUILDER: True,
            IS_REMOVABLE: False,
            STORY_PIN: {
                METADATA: {
                    PIN_TITLE: None,
                    PIN_IMAGE_SIGNATURE: None
                },
                PAGES: [{
                    BLOCKS: [{
                        BLOCK_STYLE: BLOCK_STYLE_VALUE,
                        TYPE: None
                    }],
                    LAYOUT: 0
                }]
            },
            TOPIC_TAGS: []
        }
    }
}


TITLE: str = 'title'
MEDIA_UPLOAD_ID: str = 'media_upload_id'

PIN_CONTENT_PAID_BODY: Dict[str, Any] = {
    SOURCE_URL: PAID_PIN_URL,
    DATA: {
        OPTIONS: {
            TITLE: None,
            DESCRIPTION: None,
            ALT_TEXT: None,
            BOARD_ID: None,
            LINK: None,
            IMAGE_SIGNATURE: None
        }
    }
}
