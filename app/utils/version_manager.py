# -*- coding: utf-8 -*-
# app/utils/version_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from typing import List

from requests import Response, get

from app.constants.update import VERSION_URL, CHANGELOG_URL


class VersionManager:
    """This class provides methods to retrieve tool information.

    Methods:
    --------
        retrieve_tool_version() -> str | None:
            Retrieve the version of the tool.

        retrieve_tool_changelog() -> List[str] | list:
            Retrieve the changelog of the tool.
    """
    
    @staticmethod
    def retrieve_tool_version() -> str | None:
        """Retrieve the version of the tool.
        
        This method fetches the tool version from the specified URL.
        In case of an exception (e.g., SSL error), None is returned.

        Returns:
        --------
            str | None: The tool version as a string.
        """
        try:  # Try ot get the version of the bot.
            response: Response = get(VERSION_URL, verify=False)
            if response.ok and 200 <= response.status_code < 300:
                return response.text.replace('\n', '')
        except Exception:  # SSL error.
            return None
        
    @staticmethod
    def retrieve_tool_changelog() -> List[str] | list:
        """Retrieve the changelog of the tool.

        This method fetches the tool changelog from the specified URL and
        returns it as a list of strings (one entry per line). In case of
        an exception (e.g., SSL error), an empty list is returned.

        Returns:
        --------
            List[str] | list: A list of strings containing the
                changelog entries.
        """
        try:  # Try ot get the version of the bot.
            response: Response = get(CHANGELOG_URL, verify=False)
            if response.ok and 200 <= response.status_code < 300:
                return response.text.splitlines()
            return []  # Cannot fetch the changelog URL.
        except Exception:  # SSL error.
            return []
