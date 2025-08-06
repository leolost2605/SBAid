"""
This module contains the class that represents the result manager.
"""
import gi
import sys

from sbaid.common.tag import Tag
from sbaid.model.results.result_manager import ResultManager
from sbaid.view_model.results.result import Result

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

class ResultManager(GObject.GObject):
    """ This class represents the result manager. """

    available_tags: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @available_tags.getter  # type: ignore
    def available_tags(self) -> Gio.ListModel:
        return self.__available_tags

    results: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @results.getter  # type: ignore
    def results(self):
        return self.__results

    __result_manager: ResultManager
    __available_tags: Gio.ListStore
    __results: Gio.ListStore

    def __init__(self, manager: ResultManager):
        self.__result_manager = manager
        self.__available_tags = Gio.ListStore().new(Tag)
        self.__results = Gio.ListStore().new(Result)
        super().__init__(available_tags=Gtk.MultiSelection.new(self.__result_manager.available_tags))

    def create_tag(self, name: str) -> int:
        """Creates a new tag for the result with a given name."""
        return self.__result_manager.create_tag(name)

    def delete_tag(self, tag_id: str) -> None:
        """Deletes a tag from the result with the given id."""
        self.__result_manager.delete_tag(tag_id)

    def delete_result(self, result_id: str) -> None:
        """Deletes a result from all results with the given id."""
        self.__result_manager.delete_result(result_id)