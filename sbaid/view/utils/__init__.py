"""
This module contains utils for the view.
"""

from typing import Any, Coroutine, Callable

from sbaid import common


error_reporters: list[Callable[[Exception], None]] = []


def register_error_reporter(error_reporter: Callable[[Exception], None]) -> None:
    """
    Registers a function to be called when an error occurs.
    :param error_reporter: the function to be called
    """
    error_reporters.append(error_reporter)


def run_coro_with_error_reporting(coro: Coroutine[Any, Any, None]) -> None:
    """
    Runs the given coro in the background. If an exception occurs, calls every
    registered error_reporter with the exception
    :param coro: the coro to run
    """
    common.run_coro_in_background(__coro_runner(coro))


async def __coro_runner(coro: Coroutine[Any, Any, None]) -> None:
    try:
        await coro
    except Exception as e:  # pylint: disable=broad-exception-caught
        for error_reporter in error_reporters:
            error_reporter(e)
