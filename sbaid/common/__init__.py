from typing import Any, Generator

from gi.repository import Gio


def list_model_iterator(model: Gio.ListModel) -> Generator[Any | None, Any, None]:
    for i in range(model.get_n_items() - 1):
        yield model.get_item(i)
