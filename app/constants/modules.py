# -*- coding: utf-8 -*-
# app/constants/modules.py

"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from __future__ import annotations
from typing import Dict, Final, Tuple


# Requirements for the PyQt6 module.
PYQT6: Final[Dict[str, Tuple[str, str] | Tuple]] = {
    'Windows': ('10', '11'),
    'Linux': (),
    'Darwin': ()
}

# Requirements for the PyQt5 module.
PYQT5: Final[Dict[str, Tuple[str, ...]]] = {
    'Windows': ('XP', 'Vista', '7', '8', '8.1')
}

# Required modules: {version: (prerequisites, version)}.
MODULES_LIST: Final[
        Dict[str, Tuple[Dict[str, Tuple[str, str] | Tuple] |
        Dict[str, Tuple[str, ...]] | None, str | None]]] = {
    'colorama': (None, '0.4.5'),
    'selenium': (None, '4.7.2'),
    'webdriver-manager': (None, '4.0.0'),
    'undetected-chromedriver': (None, '3.4.4'),
    'eel': (None, '0.15.3'),
    'validators': (None, '0.20.0'),
    'opencv-python': (None, None),
    'urllib3': (None, None),
    'requests': (None, None),
    'pillow': (None, None),
    'pyqt6': (PYQT6, None),
    'pyqt6-qt6': (PYQT6, None),
    'pyqt6-sip': (PYQT6, None),
    'pyqt5': (PYQT5, None),
    'pyqt5-qt5': (PYQT5, None),
    'pyqt5-sip': (PYQT5, None),
    'greenlet': (None, None),
    'gevent': (None, None),
    'pyparsing': (None, None),
    'bottle': (None, None),
    'future': (None, None),
    'tqdm': (None, None),
    'psutil': (None, None),
    'typing-extensions': (None, None),
    'screeninfo': (None, None)
}

# Formats used to install modules.
MODULE_INSTALL_FORMAT: Final[str] = '{module}=={version}'
MODULE_INSTALL_COMMAND: Final[str] = \
    '"{python}" -m pip install {modules} --force-reinstall'
