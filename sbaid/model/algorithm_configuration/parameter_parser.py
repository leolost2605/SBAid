"""This module represents the interface ParameterParser"""
from abc import ABC, abstractmethod
from typing import Callable
from gi.repository import Gio, GLib

ParameterParserForeachFunc = Callable[[str, str | None, GLib.Variant], bool]


class ParameterParser(ABC):
    """
    The interface for a parameter parser.
    """

    @abstractmethod
    def can_handle_file(self, file_path: str) -> bool:
        """
        Returns whether this parser implementation can handle the file at the given path.
        :param file_path: the path of the file to check
        :return: true if the file can be handled, false otherwise
        """

    @abstractmethod
    async def export_parameters(self, file: Gio.File,
                                foreach_func: ParameterParserForeachFunc) -> tuple[int, int]:
        """
        Parses the given file and runs the foreach func for each parameter found in the file.
        Should only be called after can_handle_file returned true for the file.
        :param file: the file to parse
        :param foreach_func: a func to call for each parameter found in the file
        :return: the number of valid parameters found and the number of invalid parameters
        """
