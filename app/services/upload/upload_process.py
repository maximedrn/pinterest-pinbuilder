from collections.abc import Callable
from datetime import datetime as dt
from datetime import timedelta
from multiprocessing import Process
from typing import Any

from app.common.data_manager import DataManager
from app.common.save_manager import SaveManager
from app.constants.messages import (
    INTERNAL,
    UPLOAD_FINISHED,
)
from app.constants.processes import UPLOAD_PROCESS
from app.services.thread_manager import ThreadManager
from app.services.upload.upload_manager import UploadManager
from app.utils.logger.console_manager import Console


class UploadProcess(DataManager, SaveManager, ThreadManager):
    """Manages the process of uploading data.

    This class handles the upload process for a given set of data. It
    retrieves data from a file, verifies its correctness, and uploads it
    using cookies. The process is multi-threaded for efficiency.

    Methods:
    --------
        __init__(
                self, file_path: str, starting_value: int,
                cookies: dict[str, Any], delete_temp_file: bool) -> None:
            Initialize the UploadProcess instance.

        upload(self) -> None:
            Start the upload process for all items in the data.

        __call__(self) -> Process:
            Initialize and start the upload process in a separate thread.

    Private methods:
    ----------------
        __upload_item(self, index: int) -> None:
            Upload an individual item from the data.

        __process_time(self, start_time: dt, end_time: dt) -> tuple[int, int]:
            Calculate and return the elapsed time in hours and minutes between
            two datetime objects.

    Attributes:
    -----------
        __starting_value (int): The starting index for data retrieval.
        __maximum_attempts (int): The limit of attempts for the upload.
        __cookies (dict[str, Any]): Cookies for authentication.
    """

    def __init__(
        self,
        file_path: str,
        starting_value: int,
        maximum_attempts: int,
        delete_temp_file: bool,
        cookies: dict[str, Any],
    ) -> None:
        """Initialize the UploadProcess instance.

        Parameters:
        -----------
            file_path (str): The path to the file containing data to upload.
            starting_value (int): The starting index for data retrieval.
            maximum_attempts (int): The limit of attempts for the upload.
            cookies (dict[str, Any]): Cookies for authentication.
            delete_temp_file (bool): Whether to delete the temporary file
                after uploading or not.
        """
        self.__starting_value: int = starting_value
        self.__maximum_attempts: int = maximum_attempts
        self.__cookies: dict[str, Any] = cookies
        DataManager.__init__(self, file_path, delete_temp_file)
        SaveManager.__init__(self, self, file_path)

    def __upload_item(self, index: int) -> None:
        """Upload an individual item from the data.

        Parameters:
        -----------
            index (int): The index of the item to upload.
        """
        # Load and verify the data according to the index.
        if not self.verify_content(index, self.file_length):
            return  # The data is not correctly formatted.
        content: dict[str, Any] = self.retrieve_content()
        attempts: int = 0  # Current attempts for the upload.
        # Run the upload with the content and cookies.
        while attempts < self.__maximum_attempts:
            if UploadManager(  # Init and call the UploadManager.
                content, self.__cookies
            )(index, self.file_length):
                self.remove_element_from_file(index + self.__starting_value)
                return  # Do not save the file and quit the function.
            attempts += 1
        self.save_upload()  # Save the file if the upload failed.

    def __process_time(self, start_time: dt, end_time: dt) -> tuple[int, int]:
        """Calculate and return the elapsed time in hours and minutes between
        two datetime objects.

        This method calculates the elapsed time between the provided start and
        end datetime objects and returns the result in hours and minutes.

        Parameters:
        -----------
            start_time (dt): The starting datetime object.
            end_time (dt): The ending datetime object.

        Returns:
        --------
            tuple[int, int]: A tuple containing the elapsed time in hours
            and minutes.
        """
        __total_time: timedelta = end_time - start_time
        hours, remainder = divmod(__total_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return hours, minutes

    def upload(self) -> None:
        """Start the upload process for all items in the data.

        This method iterates through all items in the data, uploads them,
        and removes successfully uploaded items from the data file.
        """
        __start_time: dt = dt.now()
        Console(UPLOAD_PROCESS).clear()  # Clear the console file.
        for index in range(self.__starting_value, self.file_length):
            self.__upload_item(index)
        Console(UPLOAD_PROCESS, INTERNAL).info(
            UPLOAD_FINISHED.format(
                *self.__process_time(__start_time, dt.now())
            )
        )

    def __call__(self) -> Process:
        """Initialize and start the upload process in a separate thread.

        Returns:
        --------
            Process: The running upload process thread.
        """
        __upload_method: Callable[..., None] = self.upload
        return self.run_thread_process(__upload_method)
