"""
The common module contains classes and functions that are useful
to all other sbaid modules.
"""

from typing import Any, Generator

from gi.repository import Gio


def list_model_iterator(model: Gio.ListModel) -> Generator[Any, Any, None]:
    """Iterates over a Gio.ListModel"""
    for i in range(model.get_n_items() - 1):
        yield model.get_item(i)
