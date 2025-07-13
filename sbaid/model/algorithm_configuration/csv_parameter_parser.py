"""This module defines the CSVParameterParser class."""
from gi.repository import Gio
from sbaid.model.algorithm_configuration.ParameterParser import ParameterParser, ParameterParserForeachFunc


class CSVParameterParser(ParameterParser):
    """TODO"""

    def for_each_parameter(self, file: Gio.File, callback: ParameterParserForeachFunc) -> None:
        """todo"""
        pass

    def can_handle(self, file: Gio.File) -> bool:
        """todo"""
        pass






