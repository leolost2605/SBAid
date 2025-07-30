"""todo"""

from gi.repository import Gio, GObject
from sbaid.model.results.result import Result


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
        """todo"""

    async def load_from_db(self) -> None:
        """todo"""

    def create_tag(self, name: str) -> int:
        """todo"""
        return None

    def delete_tag(self, tag_id: str) -> None:
        """todo"""

    def delete_result(self, result_id: str) -> None:
        """todo"""

    def register_result(self, result: Result) -> None:
        """todo"""
