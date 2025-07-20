"""This module defines the ResultManager class."""

from gi.repository import Gio, GObject, GLib
from sbaid.model.results.result import Result
from sbaid.common.tag import Tag


class ResultManager(GObject.GObject):
    """This class handles a list of results and tags."""

    # GObject.Property definitions
    available_tags = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    results = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self) -> None:
        """Initialize the ResultManager class."""
        super().__init__(available_tags=Gio.ListStore.new(Tag),
                         results=Gio.ListStore.new(Result))

    def load_from_db(self) -> None:
        """todo"""

    def create_tag(self, name: str) -> int:
        """Creates a new tag with the given name and adds it to the list of available tags."""
        new_tag = Tag(GLib.uuid_string_random(), name)
        self.available_tags.append(new_tag)
        return self.available_tags.find(new_tag)[1]

    def delete_tag(self, tags_id: str) -> None:
        """Removes a tag with the given id from the list of available tags,
         and removes all its uses in results"""

        n = self.available_tags.get_n_items()

        for i in range(n):
            tag = self.available_tags.get_item(i)

            if tags_id.__eq__(tag.props.tag_id):
                self.available_tags.remove(i)

                m = self.results.get_n_items()
                for a in range(m):
                    result = self.results.get_item(a)
                    result.remove_tag(tag)

                break

    def delete_result(self, result_id: str) -> None:
        """Removes a result with the given id from the list of available tags."""
        n = self.results.get_n_items()

        for i in range(n):
            if self.results.get_item(i).id.__eq__(result_id):
                self.results.remove(i)
                break

    def register_result(self, result: Result) -> None:
        """Appends a result to the existing list of results in the result manager."""
        self.results.append(result)
        # todo register to the database
