""" This module consists of the ParserFactory class and the NoSuitableParserException,
which can be raised within the ParserFactory class. """

from gi.repository import Gio
from sbaid.model.network.cross_section_parser import CrossSectionParser
from sbaid.model.network.csv_cross_section_parser import CSVCrossSectionParser


class ParserFactoryMeta(type):
    """A Metaclass for the ParserFactory, for Singleton pattern implementation."""
    _instances = {}

    def __call__(cls) -> None:
        if cls not in cls._instances:
            instance = super().__call__()
            cls._instances[cls] = instance
        return cls._instances[cls]


class ParserFactory(metaclass=ParserFactoryMeta):
    """This class handles the creation of implementations of the CrossSectionParser
    interface, as well as their assignment to user-given files."""
    __parsers: list[CrossSectionParser] = []

    def __init__(self) -> None:
        """ Constructs an instance of ParserFactory.
        Creates an instance of all implementations of CrossSectionParser and
        appends them to a parser list, to be iterated when looking for
        the correct parser of a given file."""
        self.__parsers.append(CSVCrossSectionParser())

    def get_parser(self, file: Gio.File) -> CrossSectionParser | None:
        """ Iterates the list of existing parsers and looks for one suitable to parse
         the given file. Raises a NoSuitableParserException if no such parser if found."""
        path = file.get_path()  # is an Optional str, needs to be an actual str
        for parser in self.__parsers:
            if parser.can_handle_file(path):
                return parser
        return None
