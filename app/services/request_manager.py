# -*- coding: utf-8 -*-
# app/services/request_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from io import BytesIO
from json import dumps
from typing import Any, Dict, List
from typing_extensions import deprecated
from urllib.parse import quote

from requests import post, Response

from app.constants.messages import REQUEST_ERROR
from app.constants.request_body import DATA, SOURCE_URL
from app.constants.webdriver import (
    CODE, CONTENT_TYPE, ERROR, JSON_FORMAT, MESSAGE, MESSAGE_DETAIL,
    PINTEREST_CLIENT_CONTEXT, PINTEREST_RESOURCE_RESPONSE, STATUS, SUCCESS)
from app.utils.exceptions import RequestError


class RequestManager:
    """Interface for managing requests to Pinterest.
    
    Each request requires `x-csrftoken` and cookies generated after
    connection. The class is used to create the interface for data transfer.
    
    Methods:
    --------
        __init__(self, csrf_token: str, cookies: Dict[str, str]) -> None:
            Initialize the RequestManager with the necessary
            authentication data.

        get_request_body(self, source_url: str,
                         data: Dict[str, Any]) -> Dict[str, str]:
            Generate the body for the query in dictionary format.

        post(self, url: str, body: Dict[str, Any] | None = None, 
             parameters: Dict[str, Any] | None = None,
             files: Dict[str, bytes | BytesIO] | None = None,
             resource_response: bool = True) -> Dict[str, Any]:
            Make a POST request with data as arguments.

        request_error(
                self, response: Dict[str, Any], error_message: str) -> None:
            Handle errors in upload requests by checking the response status.

    Protected methods:
    ------------------
        _is_rate_limited(self, response: Dict[str, Any]) -> bool:
            Check if an API response indicates rate limiting.

    Private methods:
    ----------------
        __format_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
            Format an error response into a standardized format.
    
        @deprecated('Not in use because cookies are not in string format.')
        __convert_cookies(self, cookies: str) -> Dict[str, Any]:
            Convert cookies in raw format into a compatible dictionary.
        
        @deprecated('Not in use because POST requests have a JSON parameter.')
        __convert_dict_to_query(self, parameters: Dict[str, Any]) -> str:
            Convert a dictionary to a URL query string.

    Attributes:
    -----------
        __headers (Dict[str, str]): The default request headers containing
            the CSRF token.
        __cookies (Dict[str, Any]): Cookies are retrieved in raw format
            after logging in to Pinterest. Each variable is separated by
            a semicolon, they are defined by an equal followed by the value.
        __extension_domain (str): The account language based on the
            extension domain of the Pinterest URL.
    """

    def __init__(self, csrf_token: str, cookies: Dict[str, str],
                 extension_domain: str) -> None:
        """Recovery of the data needed to authenticate each query.

        Parameters:
        -----------
            csrf_token (str): The token used to authenticate each and every
                request made to Pinterest's servers.
            cookies (Dict[str, Any]): Cookies are retrieved in raw format
                after logging in to Pinterest. Each variable is separated by a
                semicolon, they are defined by an equal followed by the value.
            extension_domain (str): The account language based on the
                extension domain of the Pinterest URL.
        """
        self.__headers: Dict[str, str] = {'x-csrftoken': csrf_token}
        self.__cookies: Dict[str, Any] = cookies  # self.__convert_cookies(cookies)
        self.__extension_domain: str = extension_domain
        if not self.__extension_domain.endswith('/'):
            self.__extension_domain += '/'
    
    @deprecated('Not in use because cookies are not in string format.')
    def __convert_cookies(self, cookies: str) -> Dict[str, Any]:
        """Convert cookies in raw format into a compatible dictionary.
        
        Cookies are in this format by default: "a=1; b=2; c=3".
        They are returned in this format: {"a": "1", "b": "2", "c": "3"}.
        
        Parameters:
        -----------
            cookies (str): Cookies in raw format.

        Returns:
        --------
            Dict[str, Any]: The structured dictionary of these cookies.
        """
        # "a=1; b=2" -> [("a", "1"), ("b", "2")] -> {"a": "1", "b", "2"}.
        return dict([cookie.split('=', 1) for cookie in cookies.split('; ')])
    
    @deprecated('Not in use because POST requests have a JSON parameter.')
    def __convert_dict_to_query(self, parameters: Dict[str, Any]) -> str:
        """Convert a dictionary to a URL query string.

        Parameters:
        -----------
            parameters (Dict[str, Any]): The parameters dictionary.

        Returns:
        --------
            str: The parameters in the query string format.
        """
        parameters_list: List[str] = []
        for key, value in parameters.items():
            parameters_list.append(quote(key) + '=' + quote(dumps(value)))
        return '?' + '&'.join(parameters_list)
    
    def get_request_body(
            self, source_url: str, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate the body for the query in dictionary format.
        
        Transmitted and processed data is located in the "data" key of the
        dictionary. This data is dumped for the query to work.

        Parameters:
        -----------
            source_url (str): Correspond to the front URL on Pinterest.
            data (dict): Custom query data.

        Returns:
        --------
            Dict[str, str]: The request body.
        """
        return {SOURCE_URL: source_url, DATA: dumps(data)}
    
    def post(self, url: str, body: Dict[str, Any] | None = None, 
             parameters: Dict[str, Any] | None = None,
             files: Dict[str, bytes | BytesIO] | None = None,
             resource_response: bool = True) -> Dict[str, Any]:
        """Make a POST request with data as arguments.
        
        The POST request is made by the `post()` function of `requests`
        module, adding cookies and headers.

        Parameters:
        -----------
            url (str): The domain on which the request is made.
            body (Dict[str, Any] | None, optional): The dictionary retrieved by
                the `self.get_request_body()` method. Defaults to None.
            parameters (Dict[str, Any] | None, optional): The content sent has
                a query string. Defaults to None.
            files (Dict[str, bytes | BytesIO] | None, optional): The content
                sent for the upload of a file. Defaults to None.
            resource_response (bool, optional): Determine whether only
                the resource response is required or not, Defaults to True.

        Returns:
        --------
            Dict[str, Any]: The result of the POST request.
        """
        # Add the extension domain to the URL according to the user.
        __url: str = url.format(self.__extension_domain)
        response: Response = post(  # Post the request.
            __url, headers=self.__headers, cookies=self.__cookies,
            data=body, files=files, json=parameters)
        return self.format_response(response, resource_response)
    
    def format_response(self, response: Response,
                        resource_response: bool) -> Dict[str, Any]:
        """Format the HTTP response into a structured dictionary.

        This method takes an HTTP response object and formats it into a
        structured dictionary, which may include user information or error
        messages. It also checks the HTTP status and content type to determine
        success or failure.

        - If the response is not a JSON, it returns a default error
          message if the request failed, or a success message if the request
          was successful.
        - If `resource_response` is False, only user information is extracted.
        - If `resource_response` is True, it may include error messages if the
          request was not successful.

        Parameters:
        -----------
            response (Response): The HTTP response object to be formatted.
            resource_response (bool): A flag indicating whether to extract
                resource response information.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing structured response data.
            The contents of the dictionary may include user information or
            error messages.
        """
        __ok: bool = response.ok and 200 <= response.status_code < 300
        __json: bool = JSON_FORMAT in str(response.headers.get(CONTENT_TYPE))
        if not __json:  # The response from the server is not a JSON.
            if not __ok:  # The request failed, return the default error.
                return {ERROR: REQUEST_ERROR}
            return {STATUS: SUCCESS}  # Success but no response.
        __content: Dict[str, Any] = response.json()
        if not resource_response:  # Only need the user information.
            return __content[PINTEREST_CLIENT_CONTEXT]
        __resource: Dict[str, Any] = __content[PINTEREST_RESOURCE_RESPONSE]
        if not __ok:  # Retrieve, format and return the error.
            return self.__format_error(__resource[ERROR])
        return __resource
    
    def __format_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """Format an error response into a standardized format.

        This method takes an error dictionary from an API response and formats
        it into a standardized error format, including the error message and
        error code.

        Parameters:
        -----------
            error (Dict[str, Any]): The error dictionary from an API response.

        Returns:
        --------
            Dict[str, Any]: A standardized error dictionary with 'ERROR' and
            'CODE' keys.
        """
        __error_detail: str = (': ' + error[MESSAGE_DETAIL]) \
            if MESSAGE_DETAIL in error else ''
        return {ERROR: error[MESSAGE] + __error_detail, CODE: error[CODE]}

    def request_error(
            self, response: Dict[str, Any], error_message: str) -> None:
        """Handle errors in upload requests by checking the response status.

        Parameters:
        -----------
            response (Dict[str, Any]): The response received from
                an upload request.
            error_message (str): The error message to raise in case
                of an error.

        Raises:
        -------
            RequestError: If an error is detected in the response based
                on its status.
        """
        if ERROR in response or response[STATUS] != SUCCESS:
            raise RequestError(response[ERROR] + ' (' + error_message + ')')

    def _is_rate_limited(self, response: Dict[str, Any]) -> bool:
        """Check if an API response indicates rate limiting.

        This method checks if the provided API response dictionary indicates
        that the request was rate-limited. It looks for a specific error code
        in the response.

        Parameters:
        -----------
            response (Dict[str, Any]): The API response dictionary to check.

        Returns:
        --------
            bool: True if the response indicates rate limiting,
            False otherwise.
        """
        return CODE in response and response[CODE] == 8
