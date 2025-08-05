"""
The common module contains classes and functions that are useful
to all other SBAid modules.
"""
import asyncio
from typing import Any, Generator, Coroutine

from gi.repository import Gio, GLib


def list_model_iterator(model: Gio.ListModel) -> Generator[Any, Any, None]:
    """Iterates over a Gio.ListModel"""
    for i in range(model.get_n_items()):
        yield model.get_item(i)


async def make_directory_with_parents_async(directory: Gio.File | None) -> None:
    """Creates a directory and — if they don't exist — its parents asynchronously."""
    if directory is None:
        raise FileNotFoundError("Cannot create dir with parents. No root directory found.")

    if directory.query_exists():
        return

    await make_directory_with_parents_async(directory.get_parent())

    await directory.make_directory_async(GLib.PRIORITY_DEFAULT)  # type: ignore[func-returns-value]


_background_tasks: set[asyncio.Task[None]] = set()


def _discard_task(task: asyncio.Task[None]) -> None:
    _background_tasks.discard(task)


def run_coro_in_background(coro: Coroutine[Any, Any, Any]) -> Any:
    """Runs a task in the background the fire and forget way."""
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_discard_task)
