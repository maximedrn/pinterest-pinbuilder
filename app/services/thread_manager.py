from multiprocessing import Process
from typing import Any, Callable, Iterable


class ThreadManager:
    """ThreadManager class for managing and running threaded processes.

    Methods:
    --------
        run_thread_process(
                self, method_or_function: Callable[..., None],
                args: Iterable[Any] = (),
                **kwargs: dict[str, Any]) -> Process:
            Run a threaded process with the provided method or function
            and keyword arguments.
    """

    def run_thread_process(
        self,
        method_or_function: Callable[..., None],
        args: Iterable[Any] = (),
        **kwargs: dict[str, Any],
    ) -> Process:
        """Run a threaded process with the provided method or function
        and keyword arguments.

        Parameters:
        -----------
            method_or_function (Callable[..., None]): The method or function
                to run in a separate thread.
            args (Iterable[Any], optional): Defined keywords arguments
                to pass to the method or function. Defaults to ().
            **kwargs (dict[str, Any]): Keyword arguments to pass to the
                method or function.

        Returns:
        --------
            Process: The running thread process.
        """
        self.__thread: Process = Process(
            target=method_or_function, args=args, kwargs=kwargs, daemon=True
        )
        self.__thread.start()  # Start the process.
        return self.__thread
