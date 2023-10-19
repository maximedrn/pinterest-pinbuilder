# -*- coding: utf-8 -*-
# app/services/upload/upload_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from copy import deepcopy
from io import BytesIO
from typing import Any, Dict, List, Tuple
from uuid import uuid4

from eel import sleep

from app.constants.file_settings import (
    DATETIME, FILE_PATH, IMAGE_PIN_TYPE, PAID_PIN, PINBOARD,
    PINBOARD_ID, TITLE, VIDEO_PIN_TYPE)
from app.constants.messages import (
    AMAZON_CREDENTIALS_ERROR, ETAG_ERROR, PIN, PIN_CONTENT_ERROR,
    PIN_SCHEDULE, PIN_SCHEDULED, PIN_UPLOAD, PIN_UPLOAD_ERROR,
    PIN_UPLOAD_URL, PIN_UPLOADED, PINBOARD_ID_ERROR, PINBOARDS_ERROR,
    RATE_LIMITED)
from app.constants.processes import UPLOAD_PROCESS
from app.constants.request_body import DATA, FILE, ID
from app.constants.webdriver import (
    ERROR, MESSAGE_DETAIL, PINTEREST_AMAZON_ORGANIC_URL,
    PINTEREST_AMAZON_PAID_URL, PINTEREST_ETAG_URL,
    PINTEREST_IMAGE_UPLOAD_URL, PINTEREST_MEDIA_UPLOAD_URL,
    PINTEREST_PIN_CONTENT_ORGANIC_URL, PINTEREST_PIN_CONTENT_PAID_URL,
    PINTEREST_PIN_CONTENT_SCHEDULED_ORGANIC_URL,
    PINTEREST_PIN_CONTENT_SCHEDULED_PAID_URL, PINTEREST_PINBOARD_ID_URL,
    UPLOAD_ID, UPLOAD_PARAMETERS)
from app.services.create.assets_manager import AssetsManager
from app.services.login.cookie_manager import CookieManager
from app.services.request_manager import RequestManager
from app.services.upload.upload_body import UploadBody
from app.utils.exceptions import RequestError
from app.utils.logger.console_manager import Console


class UploadManager(RequestManager, UploadBody):
    """Manage the upload process, including obtaining Amazon S3 credentials,
    uploading asset and preview files, and posting Pin content to Pinterest.

    Methods:
    --------
        __init__(self, content: Dict[str, Any],
                 cookies: Dict[str, Any]) -> None:
            Initialize the UploadManager with content and cookies.
            
        __call__(self, index: int) -> bool:
            Display the related messages and start the upload.

    Private methods:
    ----------------
        __create_uuids(self) -> Tuple[str, str]:
            Generate UUIDs for the asset and preview.

        __get_asset_settings(self) -> Tuple[str, str]:
            Get the asset settings based on the file type (image or video).

        __get_amazon_credentials(self) -> Dict[str, Dict[str, Any]]:
            Get Amazon S3 credentials for uploading.

        __get_upload_parameters(self, uuid: str) -> Dict[str, Any]:
            Get upload parameters for a specific UUID.

        __get_asset_parameters(self) -> Dict[str, Any]:
            Get upload parameters for the asset.

        __get_preview_parameters(self) -> Dict[str, Any]:
            Get upload parameters for the preview.

        __get_upload_id(self, uuid: str) -> str:
            Get the upload ID for a specific UUID.

        __get_asset_upload_id(self) -> str:
            Get the upload ID for the asset.

        __get_preview_upload_id(self) -> str:
            Get the upload ID for the preview.

        __upload_asset_file(self, parameters: Dict[str, Any]) -> None:
            Upload the asset file.

        __upload_preview_file(self, parameters: Dict[str, Any]) -> None:
            Upload the preview file.

        __get_etag(self, upload_id: str) -> str:
            Get the ETag for a specific upload.

        __upload_asset_and_get_etag(self) -> str:
            Upload the asset file and obtain its ETag.

        __upload_preview_and_get_etag(self) -> str:
            Upload the preview file and obtain its ETag.

        __get_pinboards(self) -> List[Dict[str, Any]]:
            Get a list of Pinboards.

        __get_pinboard_id(self) -> str:
            Get the ID of the target Pinboard.
            
        __get_pin_content_url(self) -> str:
            Get the URL for pin content creation based on content.

        __post_pin_content(
                self, asset_etag: str, preview_etag: str) -> Dict[str, Any]:
            Post Pin content to Pinterest.
        
        __get_title_extract(self) -> str | None:
            Get an extract of the Pin title to display.

        __start_upload(self) -> None:
            Execute the upload process, including obtaining credentials,
            uploading files, and posting Pin content.

    Attributes:
    -----------
        __content (Dict[str, Any]): The content information to be uploaded.
        __file_path (str): The file path of the asset to be uploaded.
        __file_pin_type (str): The type of the asset (image or video).
        __file_upload_url (str): The URL for uploading the asset.
        __uuids (Tuple[str, str]): A tuple of UUIDs for the asset and preview.
    """
    
    def __init__(
            self, content: Dict[str, Any], cookies: Dict[str, Any]) -> None:
        """Initialize the UploadManager with content and cookies.

        Parameters:
        -----------
            content (Dict[str, Any]): A dictionary containing information
                about the content to be uploaded.
            cookies (Dict[str, Any]): A dictionary containing cookies for
                the upload session.
        """
        self.__rate_limit: int = 10  # minutes.
        self.__content: Dict[str, Any] = deepcopy(content)
        self.__paid_pin: bool = self.__content[PAID_PIN]
        self.__file_path: str = self.__content[FILE_PATH]
        self.__uuids: Tuple[str, str] = self.__create_uuids()
        __file_settings: Tuple[str, str] = self.__get_asset_settings()
        self.__file_pin_type: str = __file_settings[0]
        self.__file_upload_url: str = __file_settings[1]
        self.__console: Console = Console(UPLOAD_PROCESS)
        super().__init__(*CookieManager.format_cookies(cookies))
    
    def __create_uuids(self) -> Tuple[str, str]:
        """Generate two random UUIDs and return them as a tuple of strings.

        This method generates two random UUIDs using the `uuid4()` function
        and returns them as a tuple of strings.

        Returns:
        --------
            Tuple[str, str]: A tuple containing two random UUIDs as strings.
        """
        return str(uuid4()), str(uuid4())
    
    def __get_asset_settings(self) -> Tuple[str, str]:
        """Get asset settings based on the asset type and return them
        as a tuple.

        This method checks the asset type based on the file path using the
        `AssetsManager` methods and returns a tuple containing the asset type
        and the corresponding Pinterest upload URL.

        Returns:
        --------
            Tuple[str, str]: A tuple containing the asset type and the
            Pinterest upload URL.

        Raises:
        --------
            Exception: If the asset type cannot be determined or is
            not supported.
        """
        if AssetsManager.is_asset_image(self.__file_path):
            return IMAGE_PIN_TYPE, PINTEREST_IMAGE_UPLOAD_URL
        if AssetsManager.is_asset_video(self.__file_path):
            return VIDEO_PIN_TYPE, PINTEREST_MEDIA_UPLOAD_URL
        raise Exception()
    
    def __get_upload_parameters(self, uuid: str) -> Dict[str, Any]:
        """Get upload parameters for a specific UUID.

        Parameters:
        -----------
            uuid (str): The UUID for which to obtain upload parameters.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing upload parameters.
        """
        # if self.__content[PAID_PIN]:
        #     return self.__amazon_credentials[UPLOAD_PARAMETERS]
        return self.__amazon_credentials[uuid][UPLOAD_PARAMETERS]
    
    def __get_asset_parameters(self) -> Dict[str, Any]:
        """Get upload parameters for the asset.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing upload
                parameters for the asset.
        """
        return self.__get_upload_parameters(self.__uuids[0])
    
    def __get_preview_parameters(self) -> Dict[str, Any]:
        """Get upload parameters for the preview.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing upload
                parameters for the preview.
        """
        return self.__get_upload_parameters(self.__uuids[1])
    
    def __get_upload_id(self, uuid: str) -> str:
        """Get the upload ID for a specific UUID.

        Parameters:
        -----------
            uuid (str): The UUID for which to obtain the upload ID.

        Returns:
        --------
            str: The upload ID.
        """
        # if self.__content[PAID_PIN]:
        #     return str(self.__amazon_credentials[UPLOAD_ID])
        return self.__amazon_credentials[uuid][UPLOAD_ID]
    
    def __get_asset_upload_id(self) -> str:
        """Get the upload ID for the asset.

        Returns:
        --------
            str: The upload ID for the asset.
        """
        return self.__get_upload_id(self.__uuids[0])
    
    def __get_preview_upload_id(self) -> str:
        """Get the upload ID for the preview.

        Returns:
        --------
            str: The upload ID for the preview.
        """
        return self.__get_upload_id(self.__uuids[1])
    
    def __get_amazon_credentials(self) -> Dict[str, Dict[str, Any]]:
        """Obtain Amazon S3 credentials for uploading the asset and preview.

        Returns:
        --------
            Dict[str, Dict[str, Any]]: A dictionary containing Amazon
                S3 credentials.
        """
        __body: Dict[str, Any] = self.get_amazon_credentials_body(
            self.__uuids, self.__file_pin_type, self.__paid_pin)
        __response: Dict[str, Any] = self.post(
            PINTEREST_AMAZON_ORGANIC_URL, parameters=__body)
        self.request_error(__response, AMAZON_CREDENTIALS_ERROR)
        return __response[DATA]
    
    def __upload_asset_file(self, parameters: Dict[str, Any]) -> None:
        """Upload the asset file to Pinterest.

        Parameters:
        -----------
            parameters (Dict[str, Any]): Upload parameters for the asset.
        """
        # Retrieve the binary content of the image/media file.
        with open(self.__file_path, 'rb') as asset_file:
            binary: bytes = asset_file.read() + str(uuid4()).encode()
        self.post(self.__file_upload_url, files={FILE: binary},
                    body=parameters)  # Upload the image/media file.
            
    def __upload_preview_file(self, parameters: Dict[str, Any]) -> None:
        """Upload the preview file to Pinterest.

        Parameters:
        -----------
            parameters (Dict[str, Any]): Upload parameters for the preview.
        """
        # Extract the preview image of the video and convert it to BytesIO.
        binary: bytes = AssetsManager.get_video_preview_file(self.__file_path)
        preview_file: BytesIO = BytesIO(binary + str(uuid4()).encode())
        self.post(PINTEREST_IMAGE_UPLOAD_URL, files={FILE: preview_file},
                  body=parameters)  # Upload the preview image file.
    
    def __get_etag(self, upload_id: str) -> str:
        """Get the ETag (entity tag) for a specific upload.

        Parameters:
        -----------
            upload_id (str): The upload ID for which to obtain the ETag.

        Returns:
        --------
            str: The ETag associated with the upload.
        """
        __body: Dict[str, Any] = self.get_etag_body(
            upload_id, self.__paid_pin)
        __response: Dict[str, Any] = self.post(  # Post the content and
            PINTEREST_ETAG_URL, parameters=__body)  # retrieve the ETag.
        self.request_error(__response, ETAG_ERROR)
        signature: str | None = __response[DATA][upload_id]['signature']
        # Return the ETag signature or makes a call to the same method.
        return signature if signature else self.__get_etag(upload_id)
    
    def __upload_asset_and_get_etag(self) -> str:
        """Upload the asset file and obtain its ETag.

        Returns:
        --------
            str: The ETag of the uploaded asset.
        """
        # Retrieve the upload parameters and upload id for the asset file.
        __asset_parameters: Dict[str, Any] = self.__get_asset_parameters()
        __asset_upload_id: str = self.__get_asset_upload_id()
        # Upload the asset file and wait until the ETag is available.
        self.__upload_asset_file(__asset_parameters)
        return self.__get_etag(__asset_upload_id)
    
    def __upload_preview_and_get_etag(self) -> str:
        """Upload the preview file and obtain its ETag.

        Returns:
        --------
            str: The ETag of the uploaded preview.
        """
        # Retrieve the upload parameters and upload id for the preview file.
        __preview_parameters: Dict[str, Any] = self.__get_preview_parameters()
        __preview_upload_id: str = self.__get_preview_upload_id()
        # Upload the preview file and wait until the ETag is available.
        self.__upload_preview_file(__preview_parameters)
        return self.__get_etag(__preview_upload_id)
    
    def __get_pinboards(self) -> List[Dict[str, Any]]:
        """Get a list of Pinboards from Pinterest.

        Returns:
        --------
            List[Dict[str, Any]]: A list of dictionaries, each
                containing Pinboard information.
        """
        __body: Dict[str, Any] = self.get_pinboard_id_body()
        __response: Dict[str, Any] = self.post(
            PINTEREST_PINBOARD_ID_URL, parameters=__body)
        self.request_error(__response, PINBOARDS_ERROR)
        return __response[DATA]['all_boards']
    
    def __get_pinboard_id(self) -> str:
        """Get the ID of the target Pinboard based on its URL.

        Returns:
        --------
            str: The ID of the Pinboard.

        Raises:
        -------
            RequestError: If the Pinboard is not found.
        """
        for pinboard in self.__get_pinboards():
            # Remove the last "/" and compare the two URLs.
            if pinboard['url'][:-1] in self.__content[PINBOARD]:
                return pinboard['id']  # Retrieve the Pinboard ID.
        raise RequestError(PINBOARD_ID_ERROR)
    
    def __get_pin_content_url(self) -> str:
        """Get the URL for pin content creation based on content.

        This method returns the URL for pin content creation based on the
        content type and whether it is a paid or organic pin. The URL is
        also determined by the presence of a scheduled date.

        Returns:
        --------
            str: The URL for pin content creation.
        """
        if self.__content[DATETIME] and self.__paid_pin:
            return PINTEREST_PIN_CONTENT_SCHEDULED_PAID_URL
        if self.__content[DATETIME] and not self.__paid_pin:
            return PINTEREST_PIN_CONTENT_SCHEDULED_ORGANIC_URL
        if not self.__content[DATETIME] and self.__paid_pin:
            return PINTEREST_PIN_CONTENT_PAID_URL
        return PINTEREST_PIN_CONTENT_ORGANIC_URL
    
    def __post_pin_content(
            self, asset_etag: str, preview_etag: str) -> Dict[str, Any]:
        """Post Pin content to Pinterest.

        Parameters:
        -----------
            asset_etag (str): The ETag of the asset.
            preview_etag (str): The ETag of the preview.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing the response
                from Pinterest after posting Pin content.
        """
        __body: Dict[str, Any] = self.get_pin_content_body(
            self.__content, asset_etag, preview_etag, self.__paid_pin)
        __url: str = self.__get_pin_content_url()
        __response: Dict[str, Any] = self.post(__url, parameters=__body)
        if not self._is_rate_limited(__response):
            self.request_error(__response, PIN_CONTENT_ERROR)
            return __response
        for remaining_time in range(self.__rate_limit, -1, -1):
            __waiting_info: str = RATE_LIMITED.format(remaining_time + 1)
            __error: str = __response[ERROR][MESSAGE_DETAIL]
            self.__console.info(__waiting_info, __error)
            sleep(60)  # Wait 1 minute before refreshing log.
        return self.__post_pin_content(asset_etag, preview_etag)
    
    def __start_upload(self) -> str:
        """Execute the upload process, including obtaining credentials,
        uploading files, and posting Pin content.
        """
        self.__amazon_credentials: Dict[str, Dict[str, Any]] = \
            self.__get_amazon_credentials()  # Get Amazon upload credentials.
        # Get the asset ETag and preview ETag (optional - same as asset).
        __asset_etag: str = self.__upload_asset_and_get_etag()
        __preview_etag: str = __asset_etag  # Default case (image).
        if AssetsManager.is_asset_video(self.__file_path):
            __preview_etag: str = self.__upload_preview_and_get_etag()
            if self.__paid_pin:  # Paid media pin requires ID, not ETag.
                __asset_etag: str = self.__get_asset_upload_id() 
        # Retrieve the Pinboard ID and post and Pin content.
        if PINBOARD in self.__content and self.__content[PINBOARD]:
            self.__content[PINBOARD_ID] = self.__get_pinboard_id()
        __response: Dict[str, Any] = self.__post_pin_content(  # Post the
            __asset_etag, __preview_etag)  # content of the Pin with ETags.
        return __response[DATA][ID]
    
    def __get_title_extract(self) -> str | None:
        """Get an extract of the Pin title to display.
        
        Returns:
        --------
            str | None: The extract of the title.
        """
        __title_length: int = 50
        __title: str | None = self.__content[TITLE]
        if __title and len(__title) > __title_length:
            return __title[:__title_length] + '...'
        return __title
    
    def __call__(self, index: int, file_length: int) -> bool:
        """Display the related messages and start the upload.
        
        Parameters:
        -----------
            index (int): The index of the current Pin.
            file_length (int): The selected file length.
        """
        try:  # Try uploading the Pin while handling the error.
            __schedule: bool = bool(self.__content[DATETIME])
            self.__console.set_title(PIN.format(index + 1, file_length))
            __title: str = PIN_SCHEDULE if __schedule else PIN_UPLOAD
            __display_title: str | None = self.__get_title_extract()
            self.__console.message(__title, __display_title)
            __pin_id: str = self.__start_upload()  # Upload the selected Pin.
            __message: str = PIN_SCHEDULED if __schedule else PIN_UPLOADED
            __url: str = PIN_UPLOAD_URL.format(id=__pin_id)
            self.__console.success(__message, __url)
            return True  # The upload has been completed.
        except (Exception, RequestError):
            self.__console.error(PIN_UPLOAD_ERROR)
            return False  # An error occurred during the Pine upload.
