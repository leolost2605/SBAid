"""This module consists of the CSV parameter parser and InvalidFileFormattingException,
which can be raised during file parsing and handling."""
import asyncio
import sys
import unittest
from gi.repository import Gio, GLib
from sbaid.model.algorithm_configuration.csv_parameter_parser import CSVParameterParser
from sbaid.model.network.csv_cross_section_parser import InvalidFileFormattingException


class CsvParameterParserTest(unittest.TestCase):
    """This class tests the csv parser using pythons unittest."""
    __background_tasks = set()

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_file_type_guesser(self):
        parser = CSVParameterParser()
        self.assertEqual(parser.can_handle
                         ("./tests/model/algorithm_configuration/valid_parameter_config.csv"),
                         True)

    def test_valid_parsing(self):
        asyncio.run(self._testing_callback_func
                    ("./tests/model/algorithm_configuration/valid_parameter_config.csv"))

    async def _testing_callback_func(self, path: str):
        parser = CSVParameterParser()
        file = Gio.File.new_for_path(path)
        await parser.for_each_parameter(file, self.foreach_func_callback_func)

    def foreach_func_callback_func(self, param_name: str, cs_id: str,
                                   variant: GLib.Variant) -> bool:
        print("param name:", param_name, "cs id:", cs_id, "variant:", variant)
        return True

    def test_invalid_parsing(self):
        with self.assertRaises(InvalidFileFormattingException):
            asyncio.run(self._testing_callback_func
                        ("./tests/model/algorithm_configuration/invalid_param_import.csv"))


