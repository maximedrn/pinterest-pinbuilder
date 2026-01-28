from typing import Any, Final

# Names of the different processes stored in the manager.
# __html: str = '.html'
__json: str = ".json"
__login: str = "login"
__upload: str = "upload"
__create: str = "create"

LOGIN_PROCESS: Final[str] = __login + __json
UPLOAD_PROCESS: Final[str] = __upload + __json
CREATE_PROCESS: Final[str] = __create + __json

PROCESSES: Final[list[str]] = [LOGIN_PROCESS, UPLOAD_PROCESS, CREATE_PROCESS]

# Keys of the `manager` global dictionary.
MANAGER_PROCESSES: Final[str] = "pid"

MANAGER_DEFAULT_STATE: Final[dict[str, Any]] = {
    MANAGER_PROCESSES: [],
    UPLOAD_PROCESS: False,
}
