from typing import Final

FILE_PATH: Final[str] = "file_path"
PINBOARD: Final[str] = "pinboard"
PINBOARD_ID: Final[str] = "pinboard_id"
TITLE: Final[str] = "title"
DESCRIPTION: Final[str] = "description"
ALT_TEXT: Final[str] = "alt_text"
LINK: Final[str] = "link"
TOPIC_TAGS: Final[str] = "topic_tags"
DATETIME: Final[str] = "datetime"
PAID_PIN: Final[str] = "paid_pin"
COOKIES: Final[str] = "cookies"
STARTING_VALUE: Final[str] = "starting_value"
MAXIMUM_ATTEMPTS: Final[str] = "maximum_attempts"
DELETE_TEMP_FILE: Final[str] = "delete_temp_file"

# JSON keys used for each element.
UPLOAD_DATA: Final[list[str]] = [
    PAID_PIN,
    FILE_PATH,
    PINBOARD,
    TITLE,
    DESCRIPTION,
    ALT_TEXT,
    LINK,
    TOPIC_TAGS,
    DATETIME,
]

TOPIC_TAGS_ID: Final[str] = "id"
TOPIC_TAGS_VALUE: Final[str] = "value"
TOPIC_TAGS_TAG_VALUE = "tagValue"
TOPIC_TAGS_KEYS: Final[list[str]] = [
    TOPIC_TAGS_ID,
    TOPIC_TAGS_VALUE,
    TOPIC_TAGS_TAG_VALUE,
]

# Constraints for certain keys used for elements.
DATA_LENGTH: Final[dict[str, int]] = {
    TITLE: 100,
    DESCRIPTION: 500,
    ALT_TEXT: 500,
}
LINK_DEFAULT_VALUE: Final[str] = "https://"
ORGANIC_PIN: Final[str] = "organic_pin"  # Paid pin already exists.

# Datetime format for `datetime.datetime` and `re`.
US_DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H-%M-%S"  # File name.
DATETIME_FORMAT: Final[str] = "%d/%m/%Y %H:%M"
JS_DATETIME_FORMAT: Final[str] = "%d/%m/%Y %H:%M"
DATETIME_FORMAT_REGEX: Final[str] = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"
JS_DATETIME_FORMAT_REGEX: Final[str] = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}"
DATETIME_SCHEDULE_LIMIT: Final[int] = 30

IMAGE_TYPE: Final[str] = "image"
VIDEO_TYPE: Final[str] = "video"
IMAGE_PIN_TYPE: Final[str] = IMAGE_TYPE + "-story-pin"
VIDEO_PIN_TYPE: Final[str] = VIDEO_TYPE + "-story-pin"
PREVIEW_MAX_WIDTH: Final[int] = 256
