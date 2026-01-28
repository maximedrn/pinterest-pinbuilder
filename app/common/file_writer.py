from json import dumps
from typing import Any


class FileWriter:
    """
    FileWriter class for writing content to a JSON file.

    Methods:
    --------
        write_content(file_path: str, content: list[dict[str, Any]]) -> None:
            Write the provided content to a JSON file.
    """

    @staticmethod
    def write_content(file_path: str, content: list[dict[str, Any]]) -> None:
        """Write the provided content to a JSON file.

        Parameters:
        -----------
            file_path (str): The path of the JSON file to write.
            content (list[dict[str, Any]]): The content to write to the file.
        """
        with open(file_path, "w+", encoding="utf-8") as file:
            file.seek(0)  # Move at the beginning of the file.
            file.truncate(0)  # Remove the content of the file.
            file.write(dumps(content, indent=4))
