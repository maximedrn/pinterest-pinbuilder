from typing import Any, Final

from app.constants.file_settings import ALT_TEXT, DESCRIPTION, LINK, TOPIC_TAGS

# Default keys of the request bodies.
SOURCE_URL: Final[str] = "source_url"
DATA: Final[str] = "data"
OPTIONS: Final[str] = "options"
URL: Final[str] = "url"

# Current sub-paths used by Pinterest.
ORGANIC_PIN_URL: Final[str] = "/pin-creation-tool/"
PAID_PIN_URL: Final[str] = "/pin-builder/"
AMAZON_UPLOAD_URL: Final[str] = "/v3/media/uploads/register/batch/"
TAGS_URL: Final[str] = "/v3/manual_tags/search/"

# User data (name and profile picture) request.
SESSION_ACCOUNTS: Final[str] = "session_accounts"

USER_DATA_BODY: Final[dict[str, Any]] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {OPTIONS: {SESSION_ACCOUNTS: True}},
}


# Tags request.
LANGUAGE: Final[str] = "language"
DEFAULT_LANGUAGE: Final[str] = "en"
QUERY: Final[str] = "query"
CORPUS: Final[str] = "corpus"
CORPUS_VALUE: Final[str] = "interests"
LIMIT: Final[str] = "limit"
MIN_LEVEL: Final[str] = "min_level"

TAGS_BODY: Final[dict[str, Any]] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {
            URL: TAGS_URL,
            DATA: {
                LANGUAGE: DEFAULT_LANGUAGE,
                QUERY: None,
                CORPUS: CORPUS_VALUE,
                LIMIT: 10,
                MIN_LEVEL: 3,
            },
        }
    },
}


# Amazon credentials request for organic Pin.
FILE: Final[str] = "file"
ID: Final[str] = "id"
MEDIA_INFO_LIST: Final[str] = "media_info_list"
MEDIA_TYPE: Final[str] = "media_type"

MEDIA_INFO_LIST_VALUE: Final[list[dict[str, Any]]] = [
    {ID: None, MEDIA_TYPE: None},
    {ID: None, MEDIA_TYPE: None},
]


AMAZON_CREDENTIALS_BODY_ORGANIC: Final[dict[str, Any]] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {OPTIONS: {URL: AMAZON_UPLOAD_URL, DATA: {MEDIA_INFO_LIST: {}}}},
}

# Amazon credentials request for paid Pin.
TYPE: Final[str] = "type"
IMAGE_PAID_PIN: Final[str] = "pinimage"
VIDEO_PAID_PIN: Final[str] = "video"

AMAZON_CREDENTIALS_BODY_PAID: Final[dict[str, Any]] = {
    SOURCE_URL: PAID_PIN_URL,
    DATA: {OPTIONS: {TYPE: None}},
}


# ETag request.
UPLOAD_IDS: Final[str] = "upload_ids"

ETAG_BODY: Final[dict[str, Any]] = {
    SOURCE_URL: None,
    DATA: {OPTIONS: {UPLOAD_IDS: []}},
}


# Pinboard ID request.
FIELD_SET_KEY: Final[str] = "field_set_key"
FIELD_SET_KEY_VALUE: Final[str] = "board_picker"
FILTER: Final[str] = "filter"
FILTER_VALUE: Final[str] = "all"

PINBOARD_ID_BODY: Final[dict[str, Any]] = {
    SOURCE_URL: ORGANIC_PIN_URL,
    DATA: {
        OPTIONS: {FIELD_SET_KEY: FIELD_SET_KEY_VALUE, FILTER: FILTER_VALUE}
    },
}

# Pin content request.
BOARD_ID: Final[str] = "board_id"
BOARD: Final[str] = "board"
SCHEDULED_TIMESTAMP: Final[str] = "scheduled_timestamp"
ALLOW_SHOPPING: Final[str] = "allow_shopping_rec"
IS_COMMENTS_ALLOWED: Final[str] = "is_comments_allowed"
IS_UNIFIED_BUILDER: Final[str] = "is_unified_builder"
IS_REMOVABLE: Final[str] = "is_removable"
STORY_PIN: Final[str] = "story_pin"
METADATA: Final[str] = "metadata"
PIN_TITLE: Final[str] = "pin_title"
PIN_IMAGE_SIGNATURE: Final[str] = "pin_image_signature"
IMAGE_SIGNATURE: Final[str] = "image_signature"
VIDEO_SIGNATURE: Final[str] = "video_signature"
PAGES: Final[str] = "pages"
BLOCKS: Final[str] = "blocks"
BLOCK_STYLE: Final[str] = "block_style"
LAYOUT: Final[str] = "layout"

BLOCK_STYLE_VALUE: Final[dict[str, int]] = {
    "height": 100,
    "width": 100,
    "x_coord": 0,
    "y_coord": 0,
}

PIN_CONTENT_ORGANIC_BODY: Final[dict[str, Any]] = {
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
                METADATA: {PIN_TITLE: None, PIN_IMAGE_SIGNATURE: None},
                PAGES: [
                    {
                        BLOCKS: [{BLOCK_STYLE: BLOCK_STYLE_VALUE, TYPE: None}],
                        LAYOUT: 0,
                    }
                ],
            },
            TOPIC_TAGS: [],
        }
    },
}


TITLE: Final[str] = "title"
MEDIA_UPLOAD_ID: Final[str] = "media_upload_id"

PIN_CONTENT_PAID_BODY: Final[dict[str, Any]] = {
    SOURCE_URL: PAID_PIN_URL,
    DATA: {
        OPTIONS: {
            TITLE: None,
            DESCRIPTION: None,
            ALT_TEXT: None,
            BOARD_ID: None,
            BOARD: None,
            LINK: None,
            IMAGE_SIGNATURE: None,
        }
    },
}
