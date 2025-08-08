"""This module represents the interface ParameterParser"""
from abc import ABC, abstractmethod
from typing import Callable, Optional, Tuple
from gi.repository import Gio, GLib

ParameterParserForeachFunc = Callable[[str, Optional[str], GLib.Variant], bool]


class ParameterParser(ABC):
    """todo"""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """todo"""

    @abstractmethod
    async def for_each_parameter(self, file: Gio.File,
                                 foreach_func: ParameterParserForeachFunc) -> Tuple[int, int]:
        """todo"""
