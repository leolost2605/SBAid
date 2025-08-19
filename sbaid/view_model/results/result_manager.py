"""
This module contains the class that represents the result manager.
"""
import sys
import gi

from sbaid.model.results.result_manager import ResultManager as ModelResultManager
from sbaid.model.results.result import Result as ModelResult
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
        """ Returns the available tags. """
        return self.__result_manager.available_tags

    results: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @results.getter  # type: ignore
    def results(self) -> Gio.ListModel:
        """ Returns the results. """
        return self.__results

    __result_manager: ModelResultManager
    __results: Gtk.MapListModel

    def __init__(self, manager: ModelResultManager):
        self.__result_manager = manager
        super().__init__(available_tags=Gtk.MultiSelection.new(
            self.__result_manager.available_tags))

        self.__results = Gtk.MapListModel.new(manager.results, self.__map_func)

    def __map_func(self, model_result: ModelResult) -> Result:
        return Result(model_result, self.available_tags)

    async def load(self) -> None:
        """
        Loads the results and their metadata. Doesn't load the actual data yet.
        """
        await self.__result_manager.load_from_db()

    async def create_tag(self, name: str) -> int:
        """Creates a new tag for the result with a given name."""
        return await self.__result_manager.create_tag(name)

    async def delete_tag(self, tag_id: str) -> None:
        """Deletes a tag from the result with the given id."""
        await self.__result_manager.delete_tag(tag_id)

    async def delete_result(self, result_id: str) -> None:
        """Deletes a result from all results with the given id."""
        await self.__result_manager.delete_result(result_id)
