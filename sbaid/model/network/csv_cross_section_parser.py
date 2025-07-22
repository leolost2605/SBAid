"""This module consists of the CSV cross section parser. TODO"""
import csv
from sbaid.model.network.cross_section_parser import (CrossSectionParser,
                                                      CrossSectionParserForeachFunc)
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate
from gi.repository import Gio


class CSVCrossSectionParser(CrossSectionParser):
    """This class handles the parsing of CSV files containing cross sections."""

    def can_handle_file(self, file_path: str) -> bool:
        """Checks if the given file is a csv file."""
        return Gio.content_type_guess(file_path)[0] == ".csv"

    async def foreach_cross_section(self, file: Gio.File,
                              foreach_func: CrossSectionParserForeachFunc) -> tuple[int, int]:
        """Loads the file contents asynchronously and reads the input CSV file row by row,
        attempting to add the cross section the row represents to the network.
        Returns the amount of added and skipped cross sections."""
        file_as_str = str(file.load_contents_async())
        if not file_as_str:  #file is empty
            raise InvalidFileFormattingException()
        csv_file_rows = file_as_str.splitlines()
        valid_cross_sections = 0
        invalid_cross_sections = 0
        if not self.__is_header(csv_file_rows[0]):
            if self.__create_from_row(csv_file_rows[0], foreach_func):
                valid_cross_sections += 1
            else:
                invalid_cross_sections += 1
        for row in csv_file_rows[1:]:
            if self.__create_from_row(row, foreach_func):
                valid_cross_sections += 1
            else:
                invalid_cross_sections += 1
        if valid_cross_sections == 0:
            raise InvalidFileFormattingException()
        return valid_cross_sections, invalid_cross_sections

    def __create_from_row(self, row: str, foreach_func: CrossSectionParserForeachFunc) -> bool:
        parsed_info = self.__parse_cross_section_syntax(row)
        if parsed_info[0]:
            if foreach_func(row[0], parsed_info[0], parsed_info[1]):
                return True
            else:
                return False
        else:
            return False

    def __is_header(self, row: str) -> bool:
        split_header_words = row.split(",")
        return (split_header_words[0].casefold() == "name"
                and split_header_words[1].casefold() == "x-coordinate"
                and split_header_words[2].casefold() == "y-coordinate"
                and split_header_words[3].casefold() == "type")

    def __parse_cross_section_syntax(self, row: str) -> (
            tuple[Coordinate, CrossSectionType] | None):
        separated_row_elements = row.split(",")
        if len(separated_row_elements) != 4:
            return None
        try:
            coordinates = Coordinate(float(separated_row_elements[1]),
                                     float(separated_row_elements[2]))
        except ValueError:
            return None
        cs_type = self.__get_enum_from_type_str(separated_row_elements[3])
        if cs_type:
            return coordinates, cs_type
        return None

    def __get_enum_from_type_str(self, cross_section_type: str) \
            -> CrossSectionType | None:
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
    """Exception raised when the user inputs a file that has
    no valid cross section definitions."""
    def __init__(self):
        self.message = "File has no valid cross section definitions."
