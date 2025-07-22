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


async def make_directory_with_parents_async(dir: Gio.File | None) -> None:
    if dir is None:
        raise FileNotFoundError("Cannot create dir with parents. No root directory found.")

    if dir.query_exists():
        return

    await make_directory_with_parents_async(dir.get_parent())

    await dir.make_directory_async(GLib.PRIORITY_DEFAULT)
