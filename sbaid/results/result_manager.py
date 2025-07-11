from gi.repository import GLib, GObject
from sbaid.results.result import Result
"""todo"""

class ResultManager:
    """todo"""

    #GObject.Property definitions
    available_tags = GObject.Property(type=str)
    results = GObject.Property(type=GLib.ListModel)

    def __init__(self) -> None:
        """todo"""
        pass

    def load_from_db(self) -> None:
        """todo"""
        pass

    def create_tag(self, name: str) -> None:
        """todo"""
        pass

    def delete_tag(self, tag_id: str) -> None:
        """todo"""
        pass

    def delete_result(self, result_id: str):
        """todo"""
        pass

    def register_result(self, result: Result) -> None:
        """todo"""
        pass
