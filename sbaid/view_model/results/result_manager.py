"""
This module contains the class that represents the result manager.
"""

import gi
import sys

from sbaid.model.results.result_manager import ResultManager

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ResultManager(GObject.GObject):
    """
    This class represents the result manager.
    """

    available_tags: Gio.ListModel = GObject.Property(  # type: ignore
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, manager: ResultManager):
        self.manager = manager
        super().__init__(available_tags=Gtk.MultiSelection.new(self.manager.available_tags))

    def create_tag(self, name: str) -> int:
        """Creates a new tag for the result with a given name."""
        return self.manager.add_tag(name)

    def delete_tag(self, name: str) -> None:
        """Deletes a tag from the result with the given name."""
        return self.manager.remove_tag(name)

    def delete_result(self, id: str) -> None:
        """Deletes a result from all results with the given id."""
        self.manager.remove_result(id)
