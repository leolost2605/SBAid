"""This module defines the CSVParameterParser class."""
import csv
import typing
import aiofiles
import ast
from gi.repository import Gio, GLib
from typing import Any

from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser, ParameterParserForeachFunc)
from sbaid.model.network.csv_cross_section_parser import InvalidFileFormattingException


class CSVParameterParser(ParameterParser):
    """This class handles the parsing of CSV files containing global and cross section parameters."""

    __blueprint_types: list[type] = []  # from the parameter configuration

    def can_handle(self, file_path: str) -> bool:
        """Checks if the given file is a csv file."""
        # TODO: Make platform independent
        return Gio.content_type_guess(file_path)[0] == ".csv"

    async def for_each_parameter(self, file: Gio.File,
                                 callback: ParameterParserForeachFunc) -> tuple[int, int]:
        """Loads the file contents asynchronously and reads the input CSV file row by row,
        attempting to add the parameter to the parameter configuration.
        Returns the amount of added and skipped parameters."""
        path = typing.cast(str, file.get_path())

        async with aiofiles.open(path, "r+") as csvfile:
            valid_parameters = 0
            invalid_parameters = 0
            csv_reader = csv.reader(csvfile)
            try:
                has_header = self.__has_valid_header(next(csv_reader))
            except StopIteration as exc:
                raise InvalidFileFormattingException() from exc
            if not has_header:
                await csvfile.seek(0)
            for row in csv_reader:
                parsed_info = self.__parse_parameter_syntax(row)
                if parsed_info is not None:




            try:
                builder = file.read(None)
                info = builder.read_all(None)[1].decode("utf-8")
                rows = info.splitlines()
                csv_reader = csv.reader(rows)
                header = next(csv_reader)
                for row in csv_reader:

                    row_info = dict(zip(header, row))
                    raw_number = row_info.get("QS_NR", '').strip()
                    cross_section = raw_number

                    for param_name, value in row_info.items():
                        if param_name == "QS_NR":
                            continue
                        value_str = value.strip()
                        if value_str == '':
                            continue

                        try:
                            if value_str == 'True':
                                variant = GLib.Variant('bool', True)
                            elif value_str == 'False':
                                variant = GLib.Variant('bool', False)
                            elif value_str == 'False':
                                variant = GLib.Variant('float', float(value_str))
                            else:
                                variant = GLib.Variant('int', int(value_str))
                        except Exception:
                            raise ValueError("Unsupported value")  #TODO assumir ser um string

                        if not callback(param_name, cross_section, variant):
                            return valid_parameters, invalid_parameters
                        valid_parameters += 1

            except Exception:
                invalid_parameters += 1

        return valid_parameters, invalid_parameters


    def __has_valid_header(self, row: list[str]) -> bool:
        return row[0].casefold() == "cs-name"

    def __compare_types(self, row: list[str]) -> bool:
        """Compares the found data types in a row with the ones given by the blueprint.
         Returns a boolean value representing the equality between the types in the
         blueprint and the given ones."""
        data_types = self.__find_types(row)
        for i, data_type in enumerate(data_types):
            if (data_type != self.__blueprint_types[i]
                    and data_type != Any):  # if the type is cell was empty
                return False
        return True

    def __find_types(self, row: list[str]) -> list[type]:
        try:
            param_type = type(ast.literal_eval(row[i]))
        except ValueError:  # if no byte, int, float, tuple, list, dict, set or None is found
            param_type = str
        except SyntaxError:
            param_type = Any  # TODO fazer depois parameter ter type None

    def __parse_cross_section_params_syntax(self, row: list[str], blueprint: list[type]) -> tuple[bool, bool]:
        """Analyses a row for correct parameter amount and types. Returns a tuple with two values:
            - a bool representing whether the parameter row is global
            - a bool representing the validity of the parameter row."""
        is_global = row[0] == ""
        if len(row) != len(blueprint):
            return False, False
        valid_counter = 0
        for i in range(len(row)):
            try:
                blueprint[i](row[i])  # cast the row value to blueprint type
                valid_counter += 1
            except ValueError:  # allow "" as valid parameter no matter the blueprint type
                if row[i] != "":
                    return False
        if valid_counter == 0:
            return False  # line is empty; skip
        return True
