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
                         ("valid_parameter_config.csv"),
                         True)

    async def _testing_callback_func(self, path: str) -> tuple[int, int]:
        parser = CSVParameterParser()
        file = Gio.File.new_for_path(path)
        return await parser.for_each_parameter(file, self.foreach_func_callback_func)

    def foreach_func_callback_func(self, param_name: str, cs_id: str,
                                   variant: GLib.Variant) -> bool:
        cs_ids = ["AQ_00_KA", "AQ_01_KA", "AQ_02_KA", "AQ_03_KA", "AQ_04_KA",
                  "AQ_05_KA", "AQ_06_KA", "AQ_07_KA"]
        params_dict = {
            "param_1" : GLib.VariantType.new("i"),
            "param_2" : GLib.VariantType.new("b"),
            "param_3" : GLib.VariantType.new("d"),
            "param_4" : GLib.VariantType.new("s"),
            "param_5" : GLib.VariantType.new("b")
        }
        if ((param_name not in params_dict.keys()
                or not variant.is_of_type(params_dict[param_name])
                or cs_id not in cs_ids)):
            return False
        return True

    def test_valid_parsing(self):
        asyncio.run(self._test_valid_parsing())

    async def _test_valid_parsing(self) -> None:
        self.assertEqual(await self._testing_callback_func("valid_parameter_config.csv"), (24, 4))

    def test_invalid_parsing(self):
        with self.assertRaises(InvalidFileFormattingException):
            asyncio.run(self._testing_callback_func
                        ("invalid_param_import.csv"))
