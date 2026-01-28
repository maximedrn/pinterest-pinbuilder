from __future__ import annotations

from multiprocessing.managers import DictProxy
from os import kill
from signal import SIGTERM
from typing import Any

from psutil import Process, process_iter
from undetected_chromedriver import Chrome

from app.constants.messages import PROCESS_HALTED
from app.constants.paths import FRONTEND_PORT
from app.constants.processes import MANAGER_PROCESSES
from app.utils.exceptions import KillListenerProcessError, KillProcessError


def save_processes(driver: Chrome) -> list[int]:
    """Save the process IDs related to the WebDriver session.

    Parameters:
    -----------
        driver (Chrome): The UC's ChromeDriver instance.

    Returns:
    --------
        list[int]: A list of process IDs.
    """
    __sub_processes: list[Any | int] = [
        driver.browser_pid,
        driver.service.process.pid,
    ]
    return [
        *__sub_processes,
        *[
            process.pid
            for process in Process(driver.service.process.pid).children(
                recursive=True
            )
        ],
    ]


def kill_processes(manager: DictProxy[Any, Any]) -> None:
    """Kill the processes specified in the manager.

    The `MANAGER_PROCESSES` key in the '`manager` dictionary should hold a
    list of process IDs (integers) to be terminated. This function iterates
    through a copy of the processes, attempts to kill each process, and
    removes it from the `MANAGER_PROCESSES` list in the `manager` dictionary
    if successful.

    Parameters:
    -----------
        manager (DictProxy[Any, Any]): A dictionary containing
            process-related information.
    """
    # Iterate through a copy of the processes.
    for process in manager[MANAGER_PROCESSES][:]:
        try:  # Try to kill the process of the webdriver.
            kill(process, SIGTERM)
        except (Exception, KillProcessError):  # Cannot kill the process.
            continue  # Continue to the next process.
        # Remove the process from the manager.
        manager[MANAGER_PROCESSES].remove(process)


def kill_listener_processes() -> None:
    """Kill listener processes associated with a specific port.

    This function is used to stop listener processes
    running on a specific port.
    """
    for process in process_iter():  # Iterate through all active processes.
        try:  # The exception may occur when `terminate()` is called.
            for connection in process.connections(kind="inet"):
                # Check that the port used by the process is one of the tool.
                if connection.laddr.port == FRONTEND_PORT:
                    process.terminate()  # Stop the process.
                    print(
                        PROCESS_HALTED.format(  # Display its information.
                            name=process.name(), pid=process.pid
                        )
                    )
        except (Exception, KillListenerProcessError):
            continue  # The process cannot be terminated.
