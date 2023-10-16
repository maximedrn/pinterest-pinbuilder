# -*- coding: utf-8 -*-
# app/services/upload/upload_body.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from copy import deepcopy
from datetime import datetime as dt
from json import dumps
from typing import Any, Dict, List, Tuple

from app.constants.file_settings import (
    ALT_TEXT, DATETIME, DATETIME_FORMAT, DESCRIPTION, IMAGE_PIN_TYPE,
    LINK, PAID_PIN, PINBOARD, TOPIC_TAGS, TITLE)
from app.constants.request_body import (
    AMAZON_CREDENTIALS_BODY_ORGANIC, AMAZON_CREDENTIALS_BODY_PAID, BLOCKS,
    BOARD_ID, DATA, ETAG_BODY, ID, IMAGE_PAID_PIN, IMAGE_SIGNATURE,
    IS_UNIFIED_BUILDER, MEDIA_INFO_LIST, MEDIA_INFO_LIST_VALUE, MEDIA_TYPE,
    MEDIA_UPLOAD_ID, METADATA, OPTIONS, ORGANIC_PIN_URL, PAGES, PAID_PIN_URL,
    PIN_CONTENT_ORGANIC_BODY, PIN_CONTENT_PAID_BODY, PIN_IMAGE_SIGNATURE,
    PIN_TITLE, PINBOARD_ID_BODY, SCHEDULED_TIMESTAMP, SOURCE_URL, STORY_PIN,
    TOPIC_TAGS, TYPE, UPLOAD_IDS, VIDEO_PAID_PIN, VIDEO_SIGNATURE)


class UploadBody:
    """Generate various JSON request bodies used in an upload process.
    
    This class provides methods for generating JSON request bodies required
    during the upload process. These request bodies are used to obtain
    Amazon S3 credentials, ETag information, Pinboard IDs, and to upload
    Pin content.
    
    Methods:
    --------
        get_pin_content_body(
                self, content: Dict[str, Any], asset_etag: str,
                preview_etag: str, paid_pin: bool) -> Dict[str, Any]:
            Generate a JSON request body for uploading Pin content.

        get_amazon_credentials_body(
                self, uuids: Tuple[str, str], file_type: str,
                paid_pin: bool) -> Dict[str, Any]:
            Generate a JSON request body for obtaining Amazon S3 credentials.

        get_etag_body(self, upload_id: str, paid_pin: bool) -> Dict[str, Any]:
            Generate a JSON request body for obtaining ETag information.

        get_pinboard_id_body(self) -> Dict[str, Any:
            Generate a JSON request body for obtaining a Pinboard ID.

    Private methods:
    ----------------
        __convert_to_timestamp(self, datetime: dt | str | None) -> int | None:
            Convert a datetime string to a timestamp in milliseconds.

        __pin_content_organic(self, content: Dict[str, Any], asset_etag: str,
                              preview_etag: str) -> Dict[str, Any]:
            Generate a JSON request body for uploading organic Pin content.

        __pin_content_paid(self, content: Dict[str, Any], asset_etag: str,
                           preview_etag: str) -> Dict[str, Any]:
            Generate a JSON request body for uploading paid Pin content.

        __amazon_credentials_organic(
                self, uuids: Tuple[str, str], file_type: str
                ) -> Dict[str, Any]:
            Generate a JSON request body for obtaining Amazon S3 credentials
            for an organic Pin.

        __amazon_credentials_paid(self, file_type: str) -> Dict[str, Any]:
            Generate a JSON request body for obtaining Amazon S3 credentials
            for a paid Pin.
    """
    
    def __amazon_credentials_organic(
            self, uuids: Tuple[str, str], file_type: str) -> Dict[str, Any]:
        """Generate a JSON request body for obtaining Amazon S3 credentials
        for an organic Pin.

        This method generates a JSON request body for obtaining Amazon S3
        credentials for an organic Pin based on the provided UUIDs and file
        type.

        Parameters:
        -----------
            uuids (Tuple[str, str]): A tuple containing two UUIDs, one for
                the asset and one for the preview.
            file_type (str): The file type of the asset.

        Returns:
        --------
            Dict[str, Any]: A JSON request body containing Amazon S3
            credentials for an organic Pin.
        """
        media_info: List[Dict[str, Any]] = deepcopy(MEDIA_INFO_LIST_VALUE)
        media_info[0][ID] = uuids[0]  # Insert the asset uuid.
        media_info[1][ID] = uuids[1]  # Insert the preview uuid.
        media_info[0][MEDIA_TYPE] = file_type  # Asset file type.
        media_info[1][MEDIA_TYPE] = IMAGE_PIN_TYPE  # Preview file type.
        amazon_credentials: Dict[str, Any] = deepcopy(
            AMAZON_CREDENTIALS_BODY_ORGANIC)
        amazon_credentials[DATA][OPTIONS][DATA][MEDIA_INFO_LIST] = \
            dumps(media_info)  # Add the string format of the media info list.
        return amazon_credentials
    
    def __amazon_credentials_paid(self, file_type: str) -> Dict[str, Any]:
        """Generate a JSON request body for obtaining Amazon S3 credentials
        for a paid Pin.

        This method generates a JSON request body for obtaining Amazon S3
        credentials for a paid Pin based on the provided file type.

        Parameters:
        -----------
            file_type (str): The file type of the asset (e.g., image or
                video).

        Returns:
        --------
            Dict[str, Any]: A JSON request body containing Amazon S3
            credentials for a paid Pin.
        """
        amazon_credentials: Dict[str, Any] = deepcopy(
            AMAZON_CREDENTIALS_BODY_PAID)
        amazon_credentials[DATA][OPTIONS][TYPE] = IMAGE_PAID_PIN \
            if IMAGE_PIN_TYPE == file_type else VIDEO_PAID_PIN
        return amazon_credentials
    
    def get_amazon_credentials_body(
            self, uuids: Tuple[str, str], file_type: str,
            paid_pin: bool) -> Dict[str, Any]:
        """Generate a JSON request body for obtaining Amazon S3 credentials.

        This method generates a JSON request body for obtaining Amazon S3
        credentials based on the provided UUIDs, file type, and whether the
        Pin is paid or organic.

        Parameters:
        -----------
            uuids (Tuple[str, str]): A tuple containing two UUIDs, one for th
                asset and one for the preview.
            file_type (str): The file type of the asset.
            paid_pin (bool): A flag indicating whether the Pin is paid (True)
                or organic (False).

        Returns:
        --------
            Dict[str, Any]: A JSON request body containing Amazon S3 credentials.
        """
        # if paid_pin:
        #     return self.__amazon_credentials_paid(file_type)
        return self.__amazon_credentials_organic(uuids, file_type)

    def get_etag_body(self, upload_id: str, paid_pin: bool) -> Dict[str, Any]:
        """Generate a JSON request body for obtaining ETag information.

        Parameters:
        -----------
            upload_id (str): The upload ID for which to obtain ETag.

        Returns:
        --------
            Dict[str, Any]: A JSON request body containing ETag information.
        """
        etag_body: Dict[str, Any] = deepcopy(ETAG_BODY)
        etag_body[SOURCE_URL] = PAID_PIN_URL if paid_pin else ORGANIC_PIN_URL
        etag_body[DATA][OPTIONS][UPLOAD_IDS] = [upload_id]
        return etag_body
    
    def get_pinboard_id_body(self) -> Dict[str, Any]:
        """Generate a JSON request body for obtaining a Pinboard ID.

        Returns:
        --------
            Dict[str, Any]: A JSON request body for obtaining a Pinboard ID.
        """
        return deepcopy(PINBOARD_ID_BODY)
    
    def __convert_to_timestamp(self, datetime: dt | str | None) -> int | None:
        """Convert a datetime string to a timestamp in milliseconds.

        This method converts a datetime string to a timestamp in milliseconds.
        If the input is not a valid datetime string or is None, it returns None.

        Parameters:
        -----------
            datetime (dt | str | None): The datetime value to convert.

        Returns:
        --------
            int | None: The timestamp in milliseconds or None if the input is
            invalid or None.
        """
        if isinstance(datetime, str) and datetime:
            __datetime: dt = dt.strptime(datetime, DATETIME_FORMAT)
            return int(round(__datetime.timestamp() * 1000))
        
    def __pin_content_organic(
            self, content: Dict[str, Any], asset_etag: str,
            preview_etag: str) -> Dict[str, Any]:
        """Generate a JSON request body for uploading organic Pin content.

        This method generates a JSON request body for uploading organic Pin
        content based on the provided content information, asset ETag,
        and preview ETag.

        Parameters:
        -----------
            content (Dict[str, Any]): A dictionary containing Pin content
                information.
            asset_etag (str): The ETag of the asset.
            preview_etag (str): The ETag of the preview.

        Returns:
        --------
            Dict[str, Any]: A JSON request body for uploading organic Pin
            content.
        """
        # Retrieve the parents' key of the parts to be edited.
        pin_content: Dict[str, Any] = deepcopy(PIN_CONTENT_ORGANIC_BODY)
        options: Dict[str, Any] = pin_content[DATA][OPTIONS]
        metadata: Dict[str, Any] = options[STORY_PIN][METADATA]
        blocks: Dict[str, Any] = options[STORY_PIN][PAGES][0][BLOCKS][0]
        # Change the source URL if it is a paid pin.
        if PAID_PIN in options and options[PAID_PIN]:
            pin_content[SOURCE_URL] = PAID_PIN_URL
        # Insert the Pin content into the different parts.
        options[DESCRIPTION] = content[DESCRIPTION]
        options[BOARD_ID] = content[PINBOARD]
        options[LINK] = content[LINK]
        options[SCHEDULED_TIMESTAMP] = self.__convert_to_timestamp(
            content[DATETIME])  # Convert the schedule datetime.
        # True if the Pin is an image, False if it is a video.
        options[IS_UNIFIED_BUILDER] = asset_etag == preview_etag
        metadata[PIN_TITLE] = content[TITLE]
        # Insert the asset and preview signature (etag).
        signature = IMAGE_SIGNATURE if asset_etag == preview_etag \
            else VIDEO_SIGNATURE  # Asset key signature (image or video).
        metadata[PIN_IMAGE_SIGNATURE] = preview_etag
        blocks[signature] = asset_etag
        # Set the Pin type (2 for image and 3 for video).
        blocks[TYPE] = 2 if asset_etag == preview_etag else 3
        options[STORY_PIN] = dumps(options[STORY_PIN])
        options[TOPIC_TAGS] = dumps(content[TOPIC_TAGS])
        return pin_content
    
    def __pin_content_paid(
            self, content: Dict[str, Any], asset_etag: str,
            preview_etag: str) -> Dict[str, Any]:
        """Generate a JSON request body for uploading paid Pin content.

        This method generates a JSON request body for uploading paid Pin
        content based on the provided content information, asset ETag,
        and preview ETag.

        Parameters:
        -----------
            content (Dict[str, Any]): A dictionary containing Pin content
                information.
            asset_etag (str): The ETag of the asset.
            preview_etag (str): The ETag of the preview.

        Returns:
        --------
            Dict[str, Any]: A JSON request body for uploading paid Pin
            content.
        """
        # Retrieve the parents' key of the parts to be edited.
        pin_content: Dict[str, Any] = deepcopy(PIN_CONTENT_PAID_BODY)
        options: Dict[str, Any] = pin_content[DATA][OPTIONS]
        options[TITLE] = content[TITLE]
        options[DESCRIPTION] = content[DESCRIPTION]
        options[ALT_TEXT] = content[ALT_TEXT]
        options[BOARD_ID], options[LINK] = content[PINBOARD], content[LINK]
        options[SCHEDULED_TIMESTAMP] = self.__convert_to_timestamp(
            content[DATETIME])  # Convert the schedule datetime.
        # True if the Pin is an image, False if it is a video.
        if asset_etag == preview_etag:  # Image.
            options[IMAGE_SIGNATURE] = asset_etag
        else:  # Asset ETag becomes media's upload ID.
            options[IMAGE_SIGNATURE] = preview_etag
            options[MEDIA_UPLOAD_ID] = asset_etag
        return pin_content
    
    def get_pin_content_body(
            self, content: Dict[str, Any], asset_etag: str,
            preview_etag: str, paid_pin: bool) -> Dict[str, Any]:
        """Generate a JSON request body for uploading Pin content.

        Parameters:
        -----------
            content (Dict[str, Any]): A dictionary containing Pin
                content information.
            asset_etag (str): The ETag of the asset.
            preview_etag (str): The ETag of the preview.

        Returns:
        --------
            Dict[str, Any]: A JSON request body for uploading Pin content.
        """
        if paid_pin:
            return self.__pin_content_paid(content, asset_etag, preview_etag)
        return self.__pin_content_organic(content, asset_etag, preview_etag)
