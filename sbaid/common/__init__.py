"""
The common module contains classes and functions that are useful
to all other sbaid modules.
"""

from typing import Any, Generator

from gi.repository import Gio, GLib


def list_model_iterator(model: Gio.ListModel) -> Generator[Any | None, Any, None]:
    """Iterates over a Gio.ListModel"""
    for i in range(model.get_n_items() - 1):
        yield model.get_item(i)


async def make_directory_with_parents_async(directory: Gio.File | None) -> None:
    """Creates a directory and - if they don't exist - its parents asynchronously."""
    if directory is None:
        raise FileNotFoundError("Cannot create dir with parents. No root directory found.")

    if directory.query_exists():
        return

    await make_directory_with_parents_async(directory.get_parent())

    await directory.make_directory_async(GLib.PRIORITY_DEFAULT)
