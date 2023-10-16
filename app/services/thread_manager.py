# -*- coding: utf-8 -*-
# app/services/thread_manager.py


"""
@author: Pinterest Pinbuilder.

Github: https://github.com/maximedrn
Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
"""


from multiprocessing import Process
from typing import Any, Callable, Dict, Iterable


class ThreadManager:
    """ThreadManager class for managing and running threaded processes.

    Methods:
    --------
        run_thread_process(
                self, method_or_function: Callable[..., None],
                args: Iterable[Any] = (),
                **kwargs: Dict[str, Any]) -> Process:
            Run a threaded process with the provided method or function
            and keyword arguments.
    """
    
    def run_thread_process(
            self, method_or_function: Callable[..., None],
            args: Iterable[Any] = (), **kwargs: Dict[str, Any]) -> Process:
        """Run a threaded process with the provided method or function
        and keyword arguments.

        Parameters:
        -----------
            method_or_function (Callable[..., None]): The method or function
                to run in a separate thread.
            args (Iterable[Any], optional): Defined keywords arguments
                to pass to the method or function. Defaults to ().
            **kwargs (Dict[str, Any]): Keyword arguments to pass to the
                method or function.

        Returns:
        --------
            Process: The running thread process.
        """
        self.__thread: Process = Process(
            target=method_or_function, args=args, kwargs=kwargs, daemon=True)
        self.__thread.start()  # Start the process.
        return self.__thread
