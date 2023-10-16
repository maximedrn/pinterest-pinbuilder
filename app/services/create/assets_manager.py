# -*- coding: utf-8 -*-
# app/services/create/assets_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from base64 import b64encode
from io import BytesIO
from mimetypes import guess_type
from typing import Any, Dict, List, Tuple

from cv2 import (
    CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, VideoCapture, imencode)
from cv2.typing import MatLike
from PIL import Image, ImageFile

from app.common.browse_manager import BrowseManager
from app.constants.file_settings import (
    FILE_PATH, IMAGE_TYPE, PREVIEW_MAX_WIDTH, VIDEO_TYPE)


class AssetsManager:
    """AssetsManager class for managing assets and their properties.

    This class provides methods for handling asset types, retrieving asset
    files, converting images and videos to base64 strings, and getting
    binary data of assets.

    Methods:
    --------
        get_asset_type(asset_file_path: str) -> str | None:
            Get the MIME type of an asset file.

        is_asset_image(asset_file_path: str) -> bool:
            Check if an asset file is an image.

        is_asset_video(asset_file_path: str) -> bool:
            Check if an asset file is a video.

        retrieve_assets_file(assets_folder: str) -> List[Dict[str, Any]]:
            Retrieve a list of asset files from a folder.

        get_image_size(image: Image.Image) -> Tuple[int, int]:
            Get the size of an image with a maximum width constraint.

        get_video_preview_file(video_file_path: str) -> bytes:
            Get a preview frame from a video file.

        get_asset_binary(asset_file_path: str) -> str:
            Get the binary data of an asset file in base64 format.

    Private methods:
    ----------------
        __image_to_base64_string(image_file_path: str) -> str:
            Get a preview frame from a video file.
    
        __video_to_base64_string(video_file_path: str) -> str:
            Convert a video file to a base64-encoded string.
    """
    
    @staticmethod
    def get_asset_type(asset_file_path: str) -> str | None:
        """Get the MIME type of an asset file.

        Parameters:
        -----------
            asset_file_path (str): The path to the asset file.

        Returns:
        --------
            str | None: The MIME type of the asset file or None
            if it cannot be determined.
        """
        __mime_type: str | None = guess_type(asset_file_path)[0]
        return __mime_type
    
    @staticmethod
    def is_asset_image(asset_file_path: str) -> bool:
        """Check if an asset file is an image.

        Parameters:
        -----------
            asset_file_path (str): The path to the asset file.

        Returns:
        --------
            bool: True if the asset is an image, False otherwise.
        """
        mime_type: str | None = AssetsManager.get_asset_type(asset_file_path)
        return str(mime_type).split('/')[0] == IMAGE_TYPE
    
    @staticmethod
    def is_asset_video(asset_file_path: str) -> bool:
        """Check if an asset file is a video.

        Parameters:
        -----------
            asset_file_path (str): The path to the asset file.

        Returns:
        --------
            bool: True if the asset is a video, False otherwise.
        """
        mime_type: str | None = AssetsManager.get_asset_type(asset_file_path)
        return str(mime_type).split('/')[0] == VIDEO_TYPE
    
    @staticmethod
    def retrieve_assets_file(assets_folder: str) -> List[Dict[str, Any]]:
        """Retrieve a list of asset files from a folder.

        Parameters:
        -----------
            assets_folder (str): The folder containing asset files.

        Returns:
        --------
            List[Dict[str, Any]]: A list of dictionaries containing
            asset file paths.
        """
        files: List[str] = BrowseManager.retrieve_files_from_folder(
            assets_folder)  # Retrieve the list of files in the folder.
        return [  # Instantiate asset paths if they are images or videos.
            {FILE_PATH: file} for file in files if AssetsManager
            .is_asset_image(file) or AssetsManager.is_asset_video(file)]
    
    @staticmethod
    def get_image_size(image: Image.Image) -> Tuple[int, int]:
        """Get the size of an image with a maximum width constraint.

        Parameters:
        -----------
            image (Image.Image): The image to get the size of.

        Returns:
        --------
            Tuple[int, int]: The size of the image (width, height)
            with a width constraint.
        """
        width, height = image.size
        return (width, height) if width <= PREVIEW_MAX_WIDTH else (
            PREVIEW_MAX_WIDTH, int(height * PREVIEW_MAX_WIDTH / width))

    @staticmethod
    def __image_to_base64_string(image_file_path: str) -> str:
        """Get a preview frame from a video file.

        Parameters:
        -----------
            video_file_path (str): The path to the video file.

        Returns:
        --------
            str: Binary data of the video preview frame.
        """
        # with open(image_file_path, 'rb') as image_file:
        #     return b64encode(image_file.read()).decode('utf-8')
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image: Image.Image = Image.open(image_file_path).convert('RGB')
        image_size: Tuple[int, int] = AssetsManager.get_image_size(image)
        image: Image.Image = image.resize(image_size)
        buffer: BytesIO = BytesIO()
        image.save(buffer, format='JPEG', quality=25)
        return b64encode(buffer.getvalue()).decode('utf-8')
        
    @staticmethod
    def get_video_preview_file(video_file_path: str) -> bytes:
        """Get the binary data of an asset file in base64 format.

        Parameters:
        -----------
            asset_file_path (str): The path to the asset file.

        Returns:
        --------
            bytes: The binary data of the asset file in base64 format.
        """
        video_capture: VideoCapture = VideoCapture(video_file_path)
        total_frames: int = int(video_capture.get(CAP_PROP_FRAME_COUNT))
        video_capture.set(CAP_PROP_POS_FRAMES, total_frames // 2)
        image: MatLike = video_capture.read()[1]
        return imencode('.jpeg', image)[1].tobytes()
    
    @staticmethod
    def __video_to_base64_string(video_file_path: str) -> str:
        """Convert a video file to a base64-encoded string.

        This method reads a video file, captures a preview frame,
        and converts it to a base64-encoded string.

        Parameters:
        -----------
            video_file_path (str): The path to the video file.

        Returns:
        --------
            str: The base64-encoded string representation of the video
            preview frame.
        """
        buffer: bytes = AssetsManager.get_video_preview_file(video_file_path)
        return b64encode(buffer).decode('utf-8')
        
    @staticmethod
    def get_asset_binary(asset_file_path: str) -> str:
        """Get the binary data of an asset file in base64 format.

        Parameters:
        -----------
            asset_file_path (str): The path to the asset file.

        Returns:
        --------
            str: The binary data of the asset file in base64 format.
        """
        if AssetsManager.is_asset_image(asset_file_path):
            return AssetsManager.__image_to_base64_string(asset_file_path)
        elif AssetsManager.is_asset_video(asset_file_path):
            return AssetsManager.__video_to_base64_string(asset_file_path)
        return ''  # The file type is unknown.
