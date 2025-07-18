"""todo"""

from gi.repository import Gio, GObject
from sbaid.model.results.result import Result
from sbaid.common.tag import Tag
import uuid


class ResultManager(GObject.GObject):
    """todo"""

    # GObject.Property definitions
    available_tags = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    results = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self) -> None:
        """todo Constructor for the ResultManager class."""
        self.available_tags = Gio.ListStore.new(Tag)
        self.results = Gio.ListStore.new(Result)

    def load_from_db(self) -> None:
        """todo"""

    def create_tag(self, name: str) -> int:
        """todo"""
        new_tag = Tag(self.__get_random_id(), name)
        self.available_tags.append(new_tag)
        return self.available_tags.find(new_tag)[1]

    def delete_tag(self, tag_id: str) -> None:
        """todo"""
        for tag in self.available_tags:
            if tag_id.__eq__(tag.get_tag_id()):
                self.available_tags.remove(tag)

    def delete_result(self, result_id: str) -> None:
        """todo"""
        for result in self.results:
            if result.id == result_id:
                result.delete()

    def register_result(self, result: Result) -> None:
        """todo"""

    def __get_random_id(self) -> str:
        # todo no need for this additional method
        return "thisisarandomidrandomlygeneratedbyme"
