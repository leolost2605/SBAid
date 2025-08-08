"""This module defines the ParserFactory class"""
import typing

from gi.repository import Gio

from sbaid.model.algorithm_configuration.csv_parameter_parser import CSVParameterParser
from sbaid.model.algorithm_configuration.parameter_parser import ParameterParser


class ParserFactoryMeta(type):
    """A Metaclass for the ParserFactory, for Singleton pattern implementation."""
    _instances: dict[type, typing.Any] = {}

    def __call__(cls) -> 'ParserFactory':
        if cls not in cls._instances:
            instance = super().__call__()
            cls._instances[cls] = instance
        return typing.cast(ParserFactory, cls._instances[cls])


class ParserFactory(metaclass=ParserFactoryMeta):
    """This class handles the creation of implementations of the Parser
    interface, as well as their assignment to user-given files."""
    __parsers: list[ParameterParser]

    def __init__(self) -> None:
        super().__init__()
        self.__parsers.append(CSVParameterParser())

    def get_parser(self, file: Gio.File) -> ParameterParser | None:
        """Iterates the list of existing parsers and looks for one suitable to parse
         the given file. Returns None if none is found."""
        path = file.get_path()
        assert isinstance(path, str)
        for parser in self.__parsers:
            if parser.can_handle_file(path):
                assert isinstance(parser, ParameterParser)
                return parser
        return None
