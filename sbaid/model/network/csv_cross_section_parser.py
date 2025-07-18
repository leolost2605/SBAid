"""This module consists of the CSV cross section parser. TODO"""
import csv
from abc import ABC
from unittest import case

from sbaid.model.network.cross_section_parser import (CrossSectionParser,
                                                      CrossSectionParserForeachFunc)
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate
from gi.repository import Gio


class CSVCrossSectionParser(CrossSectionParser, ABC):
    """This class handles the parsing of CSV files containing cross sections."""

    def can_handle_file(self, file_path: str) -> bool:
        return Gio.content_type_guess(file_path)[0] == ".csv"

    def foreach_cross_section(self, file: Gio.File,
                              foreach_func: CrossSectionParserForeachFunc) -> tuple[int, int]:
        """Reads the input CSV file row by row, representing a cross section to be imported,
        and attempts to add the cross section to the network. Returns the amount of added and skipped cross sections."""
        with open(file.get_path(), newline='') as csvfile:
            cross_section_count = (0,0)
            csv_reader = csv.reader(csvfile)
            try:
                has_header = self.__has_valid_header(csv_reader)
            except StopIteration:
                raise InvalidFileFormattingException("Empty file.")
            if not has_header:
                csvfile.seek(0)  # restart reading from the beginning of file
            for row in csv_reader:
                parsed_info = self.__parse_cross_section(row)
                if parsed_info[0]:
                    # TODO method calls for cross section creation - use foreach_func
                    # try except for exceptions that might happen when creating the cross section
                    try:
                        foreach_func(row[2], parsed_info[0], parsed_info[1])
                        cross_section_count = cross_section_count[0]+1, cross_section_count[1]
                    except ValueError:  #TODO change error - this is already checked by the parser:
                        # - create exception for already existing location etc.
                        cross_section_count = cross_section_count[0], cross_section_count[1]+1
                else:
                    next(csv_reader)
                    cross_section_count = cross_section_count[0], cross_section_count[1]+1
        if cross_section_count[0] == 0:
            raise InvalidFileFormattingException("File has no valid cross section definitions.")
        return cross_section_count


    def __convert_to_location(self, x: str, y: str) -> Coordinate | None:
        return Coordinate(float(x),float(y))

    def __has_valid_header(self, csv_reader: csv.reader) -> bool:
            row = next(csv_reader)
            return (row[0].casefold() == "Name".casefold()
                    and row[1].casefold() == "X-Coordinate".casefold()
                    and row[2].casefold() == "Y-Coordinate".casefold()
                    and row[3].casefold() == "Type".casefold())

    def __parse_cross_section(self, row: list) -> tuple[Coordinate, CrossSectionType] | None:
        if len(row) != 4:
            return None
        try:
            coordinates = Coordinate(float(row[1]),float(row[2]))
        except ValueError:
            return None
        cs_type = self.__get_enum_from_type_str(row[3])
        if cs_type:
            return coordinates, cs_type
        return None

    def __get_enum_from_type_str(self, cross_section_type: str) -> CrossSectionType | None:
        try:
            type_value = CrossSectionType[cross_section_type.upper()]
            match type_value:
                case 0:
                    return CrossSectionType.DISPLAY
                case 1:
                    return CrossSectionType.MEASURING
                case 2:
                    return CrossSectionType.COMBINED
        except KeyError:
            return None

class InvalidFileFormattingException(Exception):
    """Exception raised when the user inputs an invalid file.
    Error message is the first found invalid formatting."""
    def __init__(self, formatting_error: str):
        self.message = "Illegal file: \n %s"%formatting_error

