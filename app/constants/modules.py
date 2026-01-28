from __future__ import annotations

from typing import Final

# Requirements for the PyQt6 module.
PYQT6: Final[dict[str, tuple[str, str] | tuple]] = {
    "Windows": ("10", "11"),
    "Linux": (),
    "Darwin": (),
}

# Requirements for the PyQt5 module.
PYQT5: Final[dict[str, tuple[str, ...]]] = {
    "Windows": ("XP", "Vista", "7", "8", "8.1")
}
