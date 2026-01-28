# -*- coding: utf-8 -*-
# app/constants/license_key.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from typing import Final

from app.constants.product_id import PRODUCT_ID

# URL of the API for license key verification.
GUMROAD_API_LICENSE_URL: Final[str] = (
    'http://api.gumroad.com/v2/licenses/verify?product_id=' + str(PRODUCT_ID))

# Derived from the API URL for verification purposes.
LICENSE_KEY_COUNTER: Final[str] = GUMROAD_API_LICENSE_URL  + '&license_key={}'
LICENSE_KEY_VALIDITY: Final[str] = (
    GUMROAD_API_LICENSE_URL + '&increment_uses_count=false&license_key={}')

LICENSE_KEY: Final[str] = 'license_key'

# The regular expression for the license key format.
LICENSE_KEY_REGEX: Final[str] = r'^((.{8})\-(.{8})\-(.{8})\-(.{8}))$'
